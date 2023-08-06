import json
import warnings

from .api import LibraryWrapper, format_error
from .value import *

from opendp.whitenoise.core import api_pb2, value_pb2, base_pb2

core_wrapper = LibraryWrapper()

# All available extensions for arguments (data_n, left_lower, etc)
ALL_CONSTRAINTS = ["n", "lower", "upper", "categories"]


class Dataset(object):
    """
    Datasets represent a single tabular resource. Datasets are assumed to be private, and may be loaded from csv files or as literal arrays.

    :param path: Path to a csv file on the filesystem. It is assumed that the csv file is well-formed.
    :param value: Alternatively, a literal value/array to pass via protobuf. It is preferred to pass a path to a csv, to keep the data out of the analysis object.
    :param num_columns: The number of columns in the data resource.
    :param column_names: Alternatively, the set of column names in the data resource.
    :param value_format: If ambiguous, the data format of the value (either array, hashmap or jagged)
    :param skip_row: Set to True if the first row is the csv header. The csv header is always ignored.
    :param public: Whether to flag the data in the dataset as public. This is of course private by default.
    """

    def __init__(self, *, path=None, value=None,
                 num_columns=None, column_names=None,
                 value_format=None, skip_row=True, public=False):

        global context
        if not context:
            raise ValueError("all whitenoise components must be created within the context of an analysis")

        if sum(int(i is not None) for i in [path, value]) != 1:
            raise ValueError("either path or value must be set")

        if num_columns is None and column_names is None:
            raise ValueError("either num_columns or column_names must be set")

        self.dataset_id = context.dataset_count
        context.dataset_count += 1

        data_source = {}
        if path is not None:
            data_source['file_path'] = path
        if value is not None:
            data_source['literal'] = serialize_value(value, value_format)

        self.component = Component('Materialize',
                                   arguments={
                                       "column_names": Component.of(column_names),
                                       "num_columns": Component.of(num_columns),
                                   },
                                   options={
                                       "data_source": value_pb2.DataSource(**data_source),
                                       "public": public,
                                       "dataset_id": value_pb2.I64Null(option=self.dataset_id),
                                       "skip_row": skip_row
                                   })

    def __getitem__(self, identifier):
        return Component('Index', arguments={'columns': Component.of(identifier), 'data': self.component})


class Component(object):
    """
    Representation for the most atomic computation. There are helpers to construct these in components.py.

    The response from the helper functions are instances of this class.
    This class facilitates accessing releases, extending the graph, and viewing static properties.

    Many components are linked together to form an analysis graph.

    :param name: The id of the component. A list of component id is here: https://opendifferentialprivacy.github.io/whitenoise-core/doc/whitenoise_validator/docs/components/index.html
    :param arguments: Inputs to the component that come from prior nodes on the graph.
    :param options: Inputs to the component that are passed directly via protobuf.
    :param constraints: Additional modifiers on data inputs, like data_lower, or left_categories.
    :param value: A value that is already known about the data, to be stored in the release.
    :param value_format: The format of the value, one of `array`, `jagged`, `hashmap`
    """
    def __init__(self, name: str,
                 arguments: dict = None, options: dict = None,
                 constraints: dict = None,
                 value=None, value_format=None, value_public=False):

        accuracy = None
        if constraints:
            accuracy = constraints.get('accuracy')
            if 'accuracy' in constraints:
                del constraints['accuracy']

        self.name: str = name
        self.arguments: dict = Component._expand_constraints(arguments or {}, constraints)
        self.options: dict = options

        # these are set when add_component is called
        self.analysis = None
        self.component_id = None

        global context
        if context:
            context.add_component(self, value=value, value_format=value_format, value_public=value_public)
        else:
            raise ValueError("all whitenoise components must be created within the context of an analysis")

        if accuracy:
            privacy_usages = self.from_accuracy(accuracy['value'], accuracy['alpha'])
            print("privacy_usages", privacy_usages)
            options['privacy_usage'] = serialize_privacy_usage(privacy_usages)

        self.batch = self.analysis.batch

    # pull the released values out from the analysis' release protobuf
    @property
    def value(self):
        """
        Retrieve the released values from the analysis' release.
        If this returns None, then either analysis.release() has not yet been called, or this node is not releasable.

        :return: The value stored in the release corresponding to this node
        """
        return self.analysis.release_values.get(self.component_id, {"value": None})["value"]

    @property
    def actual_privacy_usage(self):
        """
        If a component is designed to potentially use less privacy usage than it was budgeted, this provides the reduced value

        :return: A privacy usage
        """
        return self.analysis.release_values.get(self.component_id, {"privacy_usages": None})["privacy_usages"]

    def get_parents(self):
        """
        List all nodes that use this node as a dependency/argument.
        :return: {[node_id]: [parent]}
        """
        parents = [component for component in self.analysis.components.values()
                   if id(self) in list(id(i) for i in component.arguments.values())]

        return {parent: next(k for k, v in parent.arguments.items()
                             if id(self) == id(v)) for parent in parents}

    def get_accuracy(self, alpha):
        """
        Retrieve the accuracy for the values released by the component.
        The true value differs from the estimate by at most "accuracy amount" with (1 - alpha)100% confidence.
        """
        self.analysis.update_properties()

        response = core_wrapper.privacy_usage_to_accuracy(
            privacy_definition=serialize_privacy_definition(self.analysis),
            component=serialize_component(self),
            properties={name: self.analysis.properties.get(arg.component_id) for name, arg in self.arguments.items() if arg},
            alpha=alpha)

        value = [accuracy.value for accuracy in response.values]
        if self.dimensionality <= 1 and value:
            value = value[0]
        return value

    def from_accuracy(self, value, alpha):
        """
        Retrieve the privacy usage necessary such that the true value differs from the estimate by at most "value amount" with (1 - alpha)100% confidence
        """

        self.analysis.update_properties()

        if not issubclass(type(value), list):
            value = [value for _ in range(self.num_columns)]

        if not issubclass(type(alpha), list):
            alpha = [alpha for _ in range(self.num_columns)]

        privacy_usages = core_wrapper.accuracy_to_privacy_usage(
            privacy_definition=serialize_privacy_definition(self.analysis),
            component=serialize_component(self),
            properties={name: self.analysis.properties.get(arg.component_id) for name, arg in self.arguments.items() if arg},
            accuracies=base_pb2.Accuracies(values=[
                base_pb2.Accuracy(value=value, alpha=alpha) for value, alpha in zip(value, alpha)
            ]))

        value = [parse_privacy_usage(usage) for usage in privacy_usages.values]
        if self.dimensionality <= 1 and value:
            value = value[0]
        return value

    @property
    def properties(self):
        """view protobuf representing all known properties of the component"""
        self.analysis.update_properties()
        return self.analysis.properties.get(self.component_id)

    @property
    def dimensionality(self):
        """view the statically derived dimensionality (number of axes)"""
        try:
            return self.properties.array.dimensionality
        except AttributeError:
            return None

    @property
    def nullity(self):
        """view the statically derived nullity property on the data"""
        try:
            return self.properties.array.nullity
        except AttributeError:
            return None

    @property
    def lower(self):
        """view the statically derived lower bound on the data"""
        try:
            value = parse_array1d_null(self.properties.array.continuous.minimum)
            if self.dimensionality <= 1 and value:
                value = value[0]
            return value
        except AttributeError:
            return None

    @property
    def upper(self):
        """view the statically derived upper bound on the data"""
        self.analysis.update_properties()
        try:
            value = parse_array1d_null(self.properties.array.continuous.maximum)
            if self.dimensionality <= 1 and value:
                value = value[0]
            return value
        except AttributeError:
            return None

    @property
    def num_records(self):
        """view the statically derived number of records"""
        try:
            num_records = self.properties.array.num_records
            return num_records.option if num_records.HasField("option") else None
        except AttributeError:
            return None

    @property
    def num_columns(self):
        """view the statically derived number of columns"""
        # try:
        num_columns = self.properties.array.num_columns
        return num_columns.option if num_columns.HasField("option") else None
        # except AttributeError:
        #     return None

    @property
    def data_type(self):
        """view the statically derived data type"""
        try:
            return {
                value_pb2.DataType.BOOL: "bool",
                value_pb2.DataType.I64: "int",
                value_pb2.DataType.F64: "float",
                value_pb2.DataType.STRING: "string"
            }[self.properties.array.data_type]
        except AttributeError:
            return None

    @property
    def releasable(self):
        """check if the data from this component is releasable/public"""
        try:
            return self.properties.array.releasable
        except AttributeError:
            return None

    @property
    def categories(self):
        """view the statically derived category set"""
        try:
            categories = self.properties.array.categorical.categories.data
            value = [parse_array1d_option(i) for i in categories]
            if not value:
                return None
            if self.dimensionality <= 1 and value:
                value = value[0]
            return value
        except AttributeError:
            return None

    def set(self, value):
        self.analysis.release_values[self.component_id] = {
            'value': value,
            'public': self.releasable
        }

    def __pos__(self):
        return self

    def __neg__(self):
        return Component('Negative', arguments={'data': self})

    def __add__(self, other):
        return Component('Add', {'left': self, 'right': Component.of(other)})

    def __radd__(self, other):
        return Component('Add', {'left': Component.of(other), 'right': self})

    def __sub__(self, other):
        return Component('Subtract', {'left': self, 'right': Component.of(other)})

    def __rsub__(self, other):
        return Component('Subtract', {'left': Component.of(other), 'right': self})

    def __mul__(self, other):
        return Component('Multiply', arguments={'left': self, 'right': Component.of(other)})

    def __rmul__(self, other):
        return Component('Multiply', arguments={'left': Component.of(other), 'right': self})

    def __floordiv__(self, other):
        return Component('Divide', arguments={'left': self, 'right': Component.of(other)})

    def __rfloordiv__(self, other):
        return Component('Divide', arguments={'left': Component.of(other), 'right': self})

    def __truediv__(self, other):
        return Component('Divide', arguments={
            'left': Component('Cast', arguments={'data': self}, options={"atomic_type": "float"}),
            'right': Component('Cast', arguments={'data': Component.of(other)}, options={"atomic_type": "float"})})

    def __rtruediv__(self, other):
        return Component('Divide', arguments={
            'left': Component('Cast', arguments={'data': Component.of(other)}, options={"atomic_type": "float"}),
            'right': Component('Cast', arguments={'data': self}, options={"atomic_type": "float"})})

    def __mod__(self, other):
        return Component('Modulo', arguments={'left': self, 'right': Component.of(other)})

    def __rmod__(self, other):
        return Component('Modulo', arguments={'left': Component.of(other), 'right': self})

    def __pow__(self, power, modulo=None):
        return Component('Power', arguments={'data': self, 'radical': Component.of(power)})

    def __rpow__(self, other):
        return Component('Power', arguments={'left': Component.of(other), 'right': self})

    def __or__(self, other):
        return Component('Or', arguments={'left': self, 'right': Component.of(other)})

    def __ror__(self, other):
        return Component('Or', arguments={'left': Component.of(other), 'right': self})

    def __and__(self, other):
        return Component('And', arguments={'left': self, 'right': Component.of(other)})

    def __rand__(self, other):
        return Component('And', arguments={'left': Component.of(other), 'right': self})

    def __invert__(self):
        return Component('Negate', arguments={'data': self})

    def __xor__(self, other):
        return (self | other) & ~(self & other)

    def __gt__(self, other):
        return Component('GreaterThan', arguments={'left': self, 'right': Component.of(other)})

    def __ge__(self, other):
        return Component('GreaterThan', arguments={'left': self, 'right': Component.of(other)}) \
               or Component('Equal', arguments={'left': self, 'right': Component.of(other)})

    def __lt__(self, other):
        return Component('LessThan', arguments={'left': self, 'right': Component.of(other)})

    def __le__(self, other):
        return Component('LessThan', arguments={'left': self, 'right': Component.of(other)}) \
               or Component('Equal', arguments={'left': self, 'right': Component.of(other)})

    def __eq__(self, other):
        return Component('Equal', arguments={'left': self, 'right': Component.of(other)})

    def __ne__(self, other):
        return ~(self == other)

    def __abs__(self):
        return Component('Abs', arguments={'data': self})

    def __getitem__(self, identifier):
        return Component('Index', arguments={'columns': Component.of(identifier), 'data': self})

    def __hash__(self):
        return id(self)

    def __str__(self, depth=0):
        if self.value is not None and depth != 0:
            return str(self.value).replace("\n", "")

        inner = []
        if self.arguments:
            inner.append(",\n".join([f'{("  " * (depth + 1))}{name}={value.__str__(depth + 1)}' for name, value in self.arguments.items() if value is not None]))
        if self.options:
            inner.append(",\n".join([f'{("  " * (depth + 1))}{name}={str(value).replace(chr(10), "")}' for name, value in self.options.items() if value is not None]))

        if self.name == "Literal":
            inner = "released value: " + str(self.value).replace("\n", "")
        elif inner:
            inner = f'\n{("," + chr(10)).join(inner)}\n{("  " * depth)}'
        else:
            inner = ""

        return f'{self.name}({inner})'

    def __repr__(self):
        return f'<{self.component_id}: {self.name} Component>'

    @staticmethod
    def of(value, value_format=None, public=True):
        """
        Given an array, list of lists, or dictionary, attempt to wrap it in a component and place the value in the release.
        Loose literals are by default public.
        This is an alternative constructor for a Literal, that potentially doesn't wrap the value in a Literal component if it is None or already a Component

        :param value: The value to be wrapped.
        :param value_format: must be one of `array`, `hashmap`, `jagged`
        :param public: Loose literals are by default public.
        :return: A Literal component with the value attached to the parent analysis' release.
        """
        if value is None:
            return

        # count can take the entire dataset as an argument
        if type(value) == Dataset:
            value = value.component

        if type(value) == Component:
            return value

        return Component('Literal', value=value, value_format=value_format, value_public=public)

    @staticmethod
    def _expand_constraints(arguments, constraints):
        """
        Helper function to insert additional nodes when _lower, _n, etc constraints are passed through to the component constructor utilities' kwargs.
        :param arguments: {[argument name]: [component]}
        :param constraints: restrictions on the data that will be translated into additional nodes components
        :return: a modified argument set for the current component
        """

        if not constraints:
            return arguments

        for argument in arguments.keys():
            filtered = [i[len(argument) + 1:] for i in constraints.keys()
                        if i.startswith(argument)]
            filtered = [i for i in filtered
                        if i in ALL_CONSTRAINTS]

            if 'upper' in filtered and 'lower' in filtered:
                min_component = Component.of(constraints[argument + '_lower'])
                max_component = Component.of(constraints[argument + '_upper'])

                arguments[argument] = Component('Clamp', arguments={
                    "data": arguments[argument],
                    "lower": min_component,
                    "upper": max_component
                })

                # TODO: imputation on ints is unnecessary
                arguments[argument] = Component('Impute', arguments={
                    "data": arguments[argument]
                })

            else:
                if 'upper' in filtered:
                    raise ValueError("both 'lower' and 'upper' must be specified")
                    # arguments[argument] = Component('RowMax', arguments={
                    #     "left": arguments[argument],
                    #     "right": Component.of(constraints[argument + '_upper'])
                    # })

                if 'lower' in filtered:
                    raise ValueError("both 'lower' and 'upper' must be specified")
                    # arguments[argument] = Component('RowMin', arguments={
                    #     "left": arguments[argument],
                    #     "right": Component.of(constraints[argument + '_lower'])
                    # })

            if 'categories' in filtered:
                arguments[argument] = Component('Clamp', arguments={
                    "data": arguments[argument],
                    "categories": Component.of(constraints[argument + '_categories'])
                })

            if 'n' in filtered:
                arguments[argument] = Component('Resize', arguments={
                    "data": arguments[argument],
                    "n": Component.of(constraints[argument + '_n'])
                })

            for constraint in filtered:
                del constraints[f'{argument}_{constraint}']

        if constraints:
            raise ValueError(f"unrecognized constraints: {list(constraints.keys())}")

        return arguments


class Analysis(object):
    """
    Top-level class that contains a definition of privacy and collection of statistics.
    This class tracks cumulative privacy usage for all components within.

    The dynamic flag makes the library easier to use, because multiple batches may be strung together before calling release().
    However, it opens the execution up to potential side channel attacks. Disable this if side channels are a concern.

    The eager flag makes the library easier to debug, because stack traces pass through malformed components.
    As a library user, it may be useful to enable eager and find a small, similar public dataset to help shape your analysis.
    Building an analysis with a large dataset and eager enabled is not recommended, because every additional node causes an additional release.

    Stack traces on the runtime may be disabled to help reduce the amount of leaked private information when an error is encountered.
    The library does not take into account epsilon consumed from errors.

    The filter level determines what data is included in the release.

    - `public` only newly released public data is included in the release
    - `public_and_prior` will also retain private values previously included in the release
    - `all` for including all evaluations from all nodes, which is useful for system debugging

    :param dynamic: flag for enabling dynamic validation
    :param eager: release every time a component is added
    :param distance: currently may be `pure` or `approximate`
    :param neighboring: may be `substitute` or `add_remove`
    :param stack_traces: set to False to suppress potentially sensitive stack traces
    :param filter_level: may be `public`, `public_and_prior` or `all`
    """
    def __init__(self,
                 dynamic=True, eager=False,
                 distance='approximate', neighboring='substitute',
                 stack_traces=True, filter_level='public'):

        # if false, validate the analysis before running it (enforces static validation)
        self.dynamic = dynamic

        # if true, run the analysis every time a new component is added
        self.eager = eager

        # set to false to suppress potentially private stack traces from releases
        self.stack_traces = stack_traces

        # configure to keep additional values in the release
        self.filter_level = filter_level

        if eager:
            # when eager is set, the analysis is released every time a new node is added
            warnings.warn("eager graph execution is inefficient, and should only be enabled for debugging")

        self.batch = 0

        # privacy definition
        self.distance: str = distance
        self.neighboring: str = neighboring

        # core data structures
        self.components: dict = {}
        self.release_values = {}
        self.datasets: list = []

        # track node ids
        self.component_count = 0

        # track the number of datasets in use
        self.dataset_count = 0

        # nested analyses
        self._context_cache = None

        # helper to track if properties are current
        self.properties = {}
        self.properties_id = {"count": self.component_count, "batch": self.batch}

        # stack traces for individual nodes that failed to execute
        self.warnings = []

    def add_component(self, component, value=None, value_format=None, value_public=False):
        """
        Every component must be contained in an analysis.

        :param component: The description of computation
        :param value: Optionally, the result of the computation.
        :param value_format: Optionally, the format of the result of the computation- `array` `hashmap` `jagged`
        :param value_public: set to true if the value is considered public
        :return:
        """
        if component.analysis:
            raise ValueError("this component is already a part of another analysis")

        # component should be able to reference back to the analysis to get released values/ownership
        component.analysis = self
        component.component_id = self.component_count

        if value is not None:
            self.release_values[self.component_count] = {
                'value': value,
                'value_format': value_format,
                'public': value_public
            }
        self.components[self.component_count] = component
        self.component_count += 1

        if self.eager:
            self.release()

    def update_properties(self):
        """
        If new nodes have been added or there has been a release, recompute the properties for all of the components.
        :return:
        """
        if not (self.properties_id['count'] == self.component_count and self.properties_id['batch'] == self.batch):
            response = core_wrapper.get_properties(
                serialize_analysis(self),
                serialize_release(self.release_values))

            self.properties = response.properties
            self.warnings = [format_error(warning) for warning in response.warnings]
            if self.warnings:
                warnings.warn("Some nodes were not allowed to execute.")
                self.print_warnings()
            self.properties_id = {'count': self.component_count, 'batch': self.batch}

    def validate(self):
        """
        Check if an analysis is differentially private, given a set of released values.
        This function is data agnostic. It calls the validator rust FFI with protobuf objects.

        :return: A success or failure response
        """
        return core_wrapper.validate_analysis(
            serialize_analysis(self),
            serialize_release(self.release_values)).value

    @property
    def privacy_usage(self):
        """
        Compute the overall privacy usage of an analysis.
        This function is data agnostic. It calls the validator rust FFI with protobuf objects.

        :return: A privacy usage response
        """
        return core_wrapper.compute_privacy_usage(
            serialize_analysis(self),
            serialize_release(self.release_values))

    def release(self):
        """
        Evaluate an analysis and release the differentially private results.
        This function touches private data. It calls the runtime rust FFI with protobuf objects.

        The response is stored internally in the analysis instance and the all further components are computed in the next batch.

        :return:
        """
        if not self.dynamic:
            assert self.validate(), "cannot release, analysis is not valid"

        response_proto: api_pb2.ResponseRelease.Success = core_wrapper.compute_release(
            serialize_analysis(self),
            serialize_release(self.release_values),
            self.stack_traces,
            serialize_filter_level(self.filter_level))

        self.release_values = parse_release(response_proto.release)
        self.warnings = [format_error(warning) for warning in response_proto.warnings]
        if self.warnings:
            warnings.warn("Some nodes were not allowed to execute.")
            self.print_warnings()
        self.batch += 1

    def report(self):
        """
        FFI Helper. Generate a json string with a summary/report of the Analysis and Release
        This function is data agnostic. It calls the validator rust FFI with protobuf objects.

        :return: parsed JSON array of summaries of releases
        """
        return json.loads(core_wrapper.generate_report(
            serialize_analysis(self),
            serialize_release(self.release_values)))

    def clean(self):
        """
        Remove all nodes from the analysis that do not have public descendants with released values.

        This can be helpful to clear away components that fail property checks.
        :return:
        """
        parents = {}
        for (component_id, component) in self.components.items():
            parents.setdefault(component_id, set())
            for argument in component.arguments.values():
                if argument is None:
                    continue
                parents.setdefault(argument.component_id, set()).add(component_id)
        traversal = [ident for ident, pars in parents.items() if not pars]

        while traversal:
            component_id = traversal.pop()
            component = self.components[component_id]

            # remove if properties fail to propagate to this node
            if component.releasable is None:

                # invalidate the component
                component.analysis = None
                del self.components[component_id]

                # remove this node from all children, and add children to traversal
                for argument in component.arguments.values():
                    if argument is None:
                        continue
                    parents[argument.component_id].remove(component_id)
                    traversal.append(argument.component_id)

    def enter(self):
        """
        Set the current analysis as active.
        This allows building analyses outside of context managers, in a REPL environment.
        All new Components will be attributed to the entered analysis.
        :return:
        """
        global context
        self._context = context
        context = self

    def __enter__(self):
        self.enter()
        return self

    def exit(self):
        """
        Set the current analysis as inactive.

        Components constructed after exit() will not longer be attributed to the previously active analysis.
        :return:
        """
        global context
        context = self._context

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exit()

    def print_warnings(self):
        """
        print internal warnings about failed nodes after running the graph dynamically
        """
        for warning in self.warnings:
            print(warning)

    def _make_networkx(self):
        import networkx as nx

        analysis = serialize_analysis(self)
        graph = nx.DiGraph()

        def label(node_id):
            return f'{node_id} {analysis.computation_graph.value[node_id].WhichOneof("variant")}'

        for nodeId, component in list(analysis.computation_graph.value.items()):
            for source_node_id in component.arguments.values():
                graph.add_edge(label(source_node_id), label(nodeId))

        return graph

    def plot(self):
        """
        Visual utility for graphing the analysis. Each component is a node, and arguments are edges.
        networkx and matplotlib are necessary, but must be installed separately
        :return:
        """
        import networkx as nx
        import matplotlib.pyplot as plt
        import warnings
        warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

        graph = self._make_networkx()
        nx.draw(graph, with_labels=True, node_color='white')
        plt.pause(.001)


# sugary syntax for managing analysis contexts
context = None
