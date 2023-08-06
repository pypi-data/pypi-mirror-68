"""
# cdktf

cdktf is a framework for defining cloud infrastructure using Terraform providers and modules. It allows for
users to define infrastructure resources using higher-level programming languages.

## Build

Install dependencies

```bash
yarn install
```

Build the package

```bash
yarn build
```
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import constructs

from ._jsii import *


class App(constructs.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdktf.App"):
    """Represents a cdktf application.

    stability
    :stability: experimental
    """
    def __init__(self, *, outdir: typing.Optional[str]=None) -> None:
        """Defines an app.

        :param outdir: The directory to output Terraform resources. Default: - CDKTF_OUTDIR if defined, otherwise "cdktf.out"

        stability
        :stability: experimental
        """
        options = AppOptions(outdir=outdir)

        jsii.create(App, self, [options])

    @jsii.member(jsii_name="synth")
    def synth(self) -> None:
        """Synthesizes all resources to the output directory.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synth", [])

    @builtins.property
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> str:
        """The output directory into which resources will be synthesized.

        stability
        :stability: experimental
        """
        return jsii.get(self, "outdir")


@jsii.data_type(jsii_type="cdktf.AppOptions", jsii_struct_bases=[], name_mapping={'outdir': 'outdir'})
class AppOptions():
    def __init__(self, *, outdir: typing.Optional[str]=None) -> None:
        """
        :param outdir: The directory to output Terraform resources. Default: - CDKTF_OUTDIR if defined, otherwise "cdktf.out"

        stability
        :stability: experimental
        """
        self._values = {
        }
        if outdir is not None: self._values["outdir"] = outdir

    @builtins.property
    def outdir(self) -> typing.Optional[str]:
        """The directory to output Terraform resources.

        default
        :default: - CDKTF_OUTDIR if defined, otherwise "cdktf.out"

        stability
        :stability: experimental
        """
        return self._values.get('outdir')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AppOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class BooleanMap(metaclass=jsii.JSIIMeta, jsii_type="cdktf.BooleanMap"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, terraform_resource: "TerraformResource", terraform_attribute: str) -> None:
        """
        :param terraform_resource: -
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        jsii.create(BooleanMap, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="lookup")
    def lookup(self, key: str) -> bool:
        """
        :param key: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "lookup", [key])

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformAttribute")

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: str):
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> "TerraformResource":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformResource")

    @_terraform_resource.setter
    def _terraform_resource(self, value: "TerraformResource"):
        jsii.set(self, "terraformResource", value)


class ComplexComputedList(metaclass=jsii.JSIIMeta, jsii_type="cdktf.ComplexComputedList"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, terraform_resource: "TerraformResource", terraform_attribute: str, index: str) -> None:
        """
        :param terraform_resource: -
        :param terraform_attribute: -
        :param index: -

        stability
        :stability: experimental
        """
        jsii.create(ComplexComputedList, self, [terraform_resource, terraform_attribute, index])

    @jsii.member(jsii_name="getListAttribute")
    def get_list_attribute(self, terraform_attribute: str) -> typing.List[str]:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getListAttribute", [terraform_attribute])

    @jsii.member(jsii_name="getNumberAttribute")
    def get_number_attribute(self, terraform_attribute: str) -> jsii.Number:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getNumberAttribute", [terraform_attribute])

    @jsii.member(jsii_name="getStringAttribute")
    def get_string_attribute(self, terraform_attribute: str) -> str:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getStringAttribute", [terraform_attribute])

    @jsii.member(jsii_name="interpolationForAttribute")
    def _interpolation_for_attribute(self, property: str) -> str:
        """
        :param property: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "interpolationForAttribute", [property])

    @builtins.property
    @jsii.member(jsii_name="index")
    def _index(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "index")

    @_index.setter
    def _index(self, value: str):
        jsii.set(self, "index", value)

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformAttribute")

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: str):
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> "TerraformResource":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformResource")

    @_terraform_resource.setter
    def _terraform_resource(self, value: "TerraformResource"):
        jsii.set(self, "terraformResource", value)


class NumberMap(metaclass=jsii.JSIIMeta, jsii_type="cdktf.NumberMap"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, terraform_resource: "TerraformResource", terraform_attribute: str) -> None:
        """
        :param terraform_resource: -
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        jsii.create(NumberMap, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="lookup")
    def lookup(self, key: str) -> jsii.Number:
        """
        :param key: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "lookup", [key])

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformAttribute")

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: str):
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> "TerraformResource":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformResource")

    @_terraform_resource.setter
    def _terraform_resource(self, value: "TerraformResource"):
        jsii.set(self, "terraformResource", value)


class StringMap(metaclass=jsii.JSIIMeta, jsii_type="cdktf.StringMap"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, terraform_resource: "TerraformResource", terraform_attribute: str) -> None:
        """
        :param terraform_resource: -
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        jsii.create(StringMap, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="lookup")
    def lookup(self, key: str) -> str:
        """
        :param key: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "lookup", [key])

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformAttribute")

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: str):
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> "TerraformResource":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformResource")

    @_terraform_resource.setter
    def _terraform_resource(self, value: "TerraformResource"):
        jsii.set(self, "terraformResource", value)


class TerraformElement(constructs.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdktf.TerraformElement"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, scope: constructs.Construct, id: str, *, node_factory: typing.Optional[constructs.INodeFactory]=None) -> None:
        """Creates a new construct node.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings. If the ID includes a path separator (``/``), then it will be replaced by double dash ``--``.
        :param node_factory: A factory for attaching ``Node``s to the construct. Default: - the default ``Node`` is associated
        """
        options = constructs.ConstructOptions(node_factory=node_factory)

        jsii.create(TerraformElement, self, [scope, id, options])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toTerraform", [])


@jsii.data_type(jsii_type="cdktf.TerraformGeneratorMetadata", jsii_struct_bases=[], name_mapping={'provider_name': 'providerName', 'provider_version_constraint': 'providerVersionConstraint'})
class TerraformGeneratorMetadata():
    def __init__(self, *, provider_name: str, provider_version_constraint: typing.Optional[str]=None) -> None:
        """
        :param provider_name: 
        :param provider_version_constraint: 

        stability
        :stability: experimental
        """
        self._values = {
            'provider_name': provider_name,
        }
        if provider_version_constraint is not None: self._values["provider_version_constraint"] = provider_version_constraint

    @builtins.property
    def provider_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('provider_name')

    @builtins.property
    def provider_version_constraint(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('provider_version_constraint')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TerraformGeneratorMetadata(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="cdktf.TerraformMetaArguments", jsii_struct_bases=[], name_mapping={'count': 'count', 'depends_on': 'dependsOn', 'lifecycle': 'lifecycle', 'provider': 'provider'})
class TerraformMetaArguments():
    def __init__(self, *, count: typing.Optional[jsii.Number]=None, depends_on: typing.Optional[typing.List["TerraformResource"]]=None, lifecycle: typing.Optional["TerraformResourceLifecycle"]=None, provider: typing.Optional["TerraformProvider"]=None) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 

        stability
        :stability: experimental
        """
        if isinstance(lifecycle, dict): lifecycle = TerraformResourceLifecycle(**lifecycle)
        self._values = {
        }
        if count is not None: self._values["count"] = count
        if depends_on is not None: self._values["depends_on"] = depends_on
        if lifecycle is not None: self._values["lifecycle"] = lifecycle
        if provider is not None: self._values["provider"] = provider

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('count')

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List["TerraformResource"]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('depends_on')

    @builtins.property
    def lifecycle(self) -> typing.Optional["TerraformResourceLifecycle"]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('lifecycle')

    @builtins.property
    def provider(self) -> typing.Optional["TerraformProvider"]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('provider')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TerraformMetaArguments(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class TerraformModule(TerraformElement, metaclass=jsii.JSIIAbstractClass, jsii_type="cdktf.TerraformModule"):
    """
    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _TerraformModuleProxy

    def __init__(self, scope: constructs.Construct, id: str, *, source: str, version: str) -> None:
        """
        :param scope: -
        :param id: -
        :param source: 
        :param version: 

        stability
        :stability: experimental
        """
        options = TerraformModuleOptions(source=source, version=version)

        jsii.create(TerraformModule, self, [scope, id, options])

    @jsii.member(jsii_name="interpolationForOutput")
    def interpolation_for_output(self, module_output: str) -> typing.Any:
        """
        :param module_output: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "interpolationForOutput", [module_output])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toTerraform", [])

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "source")

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "version")


class _TerraformModuleProxy(TerraformModule):
    pass

@jsii.data_type(jsii_type="cdktf.TerraformModuleOptions", jsii_struct_bases=[], name_mapping={'source': 'source', 'version': 'version'})
class TerraformModuleOptions():
    def __init__(self, *, source: str, version: str) -> None:
        """
        :param source: 
        :param version: 

        stability
        :stability: experimental
        """
        self._values = {
            'source': source,
            'version': version,
        }

    @builtins.property
    def source(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('source')

    @builtins.property
    def version(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TerraformModuleOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class TerraformOutput(TerraformElement, metaclass=jsii.JSIIMeta, jsii_type="cdktf.TerraformOutput"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, scope: constructs.Construct, id: str, *, depends_on: typing.Optional[typing.List["TerraformResource"]]=None, description: typing.Optional[str]=None, sensitive: typing.Optional[bool]=None, value: typing.Optional[typing.Union[typing.Optional[str], typing.Optional[jsii.Number], typing.Optional[bool], typing.Optional[typing.List[typing.Any]], typing.Optional[typing.Mapping[str, typing.Any]]]]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param depends_on: 
        :param description: 
        :param sensitive: 
        :param value: 

        stability
        :stability: experimental
        """
        config = TerraformOutputConfig(depends_on=depends_on, description=description, sensitive=sensitive, value=value)

        jsii.create(TerraformOutput, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toTerraform", [])

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> typing.Optional[typing.List["TerraformResource"]]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "dependsOn")

    @depends_on.setter
    def depends_on(self, value: typing.Optional[typing.List["TerraformResource"]]):
        jsii.set(self, "dependsOn", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="sensitive")
    def sensitive(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "sensitive")

    @sensitive.setter
    def sensitive(self, value: typing.Optional[bool]):
        jsii.set(self, "sensitive", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Optional[typing.Union[typing.Optional[str], typing.Optional[jsii.Number], typing.Optional[bool], typing.Optional[typing.List[typing.Any]], typing.Optional[typing.Mapping[str, typing.Any]]]]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "value")

    @value.setter
    def value(self, value: typing.Optional[typing.Union[typing.Optional[str], typing.Optional[jsii.Number], typing.Optional[bool], typing.Optional[typing.List[typing.Any]], typing.Optional[typing.Mapping[str, typing.Any]]]]):
        jsii.set(self, "value", value)


@jsii.data_type(jsii_type="cdktf.TerraformOutputConfig", jsii_struct_bases=[], name_mapping={'depends_on': 'dependsOn', 'description': 'description', 'sensitive': 'sensitive', 'value': 'value'})
class TerraformOutputConfig():
    def __init__(self, *, depends_on: typing.Optional[typing.List["TerraformResource"]]=None, description: typing.Optional[str]=None, sensitive: typing.Optional[bool]=None, value: typing.Optional[typing.Union[typing.Optional[str], typing.Optional[jsii.Number], typing.Optional[bool], typing.Optional[typing.List[typing.Any]], typing.Optional[typing.Mapping[str, typing.Any]]]]=None) -> None:
        """
        :param depends_on: 
        :param description: 
        :param sensitive: 
        :param value: 

        stability
        :stability: experimental
        """
        self._values = {
        }
        if depends_on is not None: self._values["depends_on"] = depends_on
        if description is not None: self._values["description"] = description
        if sensitive is not None: self._values["sensitive"] = sensitive
        if value is not None: self._values["value"] = value

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List["TerraformResource"]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('depends_on')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('description')

    @builtins.property
    def sensitive(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('sensitive')

    @builtins.property
    def value(self) -> typing.Optional[typing.Union[typing.Optional[str], typing.Optional[jsii.Number], typing.Optional[bool], typing.Optional[typing.List[typing.Any]], typing.Optional[typing.Mapping[str, typing.Any]]]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('value')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TerraformOutputConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class TerraformProvider(TerraformElement, metaclass=jsii.JSIIAbstractClass, jsii_type="cdktf.TerraformProvider"):
    """
    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _TerraformProviderProxy

    def __init__(self, scope: constructs.Construct, id: str, *, terraform_resource_type: str, terraform_generator_metadata: typing.Optional["TerraformGeneratorMetadata"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param terraform_resource_type: 
        :param terraform_generator_metadata: 

        stability
        :stability: experimental
        """
        config = TerraformProviderConfig(terraform_resource_type=terraform_resource_type, terraform_generator_metadata=terraform_generator_metadata)

        jsii.create(TerraformProvider, self, [scope, id, config])

    @jsii.member(jsii_name="addOverride")
    def add_override(self, path: str, value: typing.Any) -> None:
        """
        :param path: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addOverride", [path, value])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        """Adds this resource to the terraform JSON output.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toTerraform", [])

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "fqn")

    @builtins.property
    @jsii.member(jsii_name="metaAttributes")
    def meta_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "metaAttributes")

    @builtins.property
    @jsii.member(jsii_name="terraformResourceType")
    def terraform_resource_type(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformResourceType")

    @builtins.property
    @jsii.member(jsii_name="terraformGeneratorMetadata")
    def terraform_generator_metadata(self) -> typing.Optional["TerraformGeneratorMetadata"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformGeneratorMetadata")

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "alias")

    @alias.setter
    def alias(self, value: typing.Optional[str]):
        jsii.set(self, "alias", value)


class _TerraformProviderProxy(TerraformProvider):
    pass

@jsii.data_type(jsii_type="cdktf.TerraformProviderConfig", jsii_struct_bases=[], name_mapping={'terraform_resource_type': 'terraformResourceType', 'terraform_generator_metadata': 'terraformGeneratorMetadata'})
class TerraformProviderConfig():
    def __init__(self, *, terraform_resource_type: str, terraform_generator_metadata: typing.Optional["TerraformGeneratorMetadata"]=None) -> None:
        """
        :param terraform_resource_type: 
        :param terraform_generator_metadata: 

        stability
        :stability: experimental
        """
        if isinstance(terraform_generator_metadata, dict): terraform_generator_metadata = TerraformGeneratorMetadata(**terraform_generator_metadata)
        self._values = {
            'terraform_resource_type': terraform_resource_type,
        }
        if terraform_generator_metadata is not None: self._values["terraform_generator_metadata"] = terraform_generator_metadata

    @builtins.property
    def terraform_resource_type(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('terraform_resource_type')

    @builtins.property
    def terraform_generator_metadata(self) -> typing.Optional["TerraformGeneratorMetadata"]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('terraform_generator_metadata')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TerraformProviderConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class TerraformResource(TerraformElement, metaclass=jsii.JSIIMeta, jsii_type="cdktf.TerraformResource"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, scope: constructs.Construct, id: str, *, terraform_resource_type: str, terraform_generator_metadata: typing.Optional["TerraformGeneratorMetadata"]=None, count: typing.Optional[jsii.Number]=None, depends_on: typing.Optional[typing.List["TerraformResource"]]=None, lifecycle: typing.Optional["TerraformResourceLifecycle"]=None, provider: typing.Optional["TerraformProvider"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param terraform_resource_type: 
        :param terraform_generator_metadata: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 

        stability
        :stability: experimental
        """
        config = TerraformResourceConfig(terraform_resource_type=terraform_resource_type, terraform_generator_metadata=terraform_generator_metadata, count=count, depends_on=depends_on, lifecycle=lifecycle, provider=provider)

        jsii.create(TerraformResource, self, [scope, id, config])

    @jsii.member(jsii_name="addOverride")
    def add_override(self, path: str, value: typing.Any) -> None:
        """
        :param path: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addOverride", [path, value])

    @jsii.member(jsii_name="getBooleanAttribute")
    def get_boolean_attribute(self, terraform_attribute: str) -> bool:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getBooleanAttribute", [terraform_attribute])

    @jsii.member(jsii_name="getListAttribute")
    def get_list_attribute(self, terraform_attribute: str) -> typing.List[str]:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getListAttribute", [terraform_attribute])

    @jsii.member(jsii_name="getNumberAttribute")
    def get_number_attribute(self, terraform_attribute: str) -> jsii.Number:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getNumberAttribute", [terraform_attribute])

    @jsii.member(jsii_name="getStringAttribute")
    def get_string_attribute(self, terraform_attribute: str) -> str:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getStringAttribute", [terraform_attribute])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        """Adds this resource to the terraform JSON output.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toTerraform", [])

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "fqn")

    @builtins.property
    @jsii.member(jsii_name="terraformMetaArguments")
    def terraform_meta_arguments(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformMetaArguments")

    @builtins.property
    @jsii.member(jsii_name="terraformResourceType")
    def terraform_resource_type(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformResourceType")

    @builtins.property
    @jsii.member(jsii_name="terraformGeneratorMetadata")
    def terraform_generator_metadata(self) -> typing.Optional["TerraformGeneratorMetadata"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformGeneratorMetadata")

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "count")

    @count.setter
    def count(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "count", value)

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> typing.Optional[typing.List["TerraformResource"]]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "dependsOn")

    @depends_on.setter
    def depends_on(self, value: typing.Optional[typing.List["TerraformResource"]]):
        jsii.set(self, "dependsOn", value)

    @builtins.property
    @jsii.member(jsii_name="lifecycle")
    def lifecycle(self) -> typing.Optional["TerraformResourceLifecycle"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "lifecycle")

    @lifecycle.setter
    def lifecycle(self, value: typing.Optional["TerraformResourceLifecycle"]):
        jsii.set(self, "lifecycle", value)

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> typing.Optional["TerraformProvider"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "provider")

    @provider.setter
    def provider(self, value: typing.Optional["TerraformProvider"]):
        jsii.set(self, "provider", value)


@jsii.data_type(jsii_type="cdktf.TerraformResourceConfig", jsii_struct_bases=[TerraformMetaArguments], name_mapping={'count': 'count', 'depends_on': 'dependsOn', 'lifecycle': 'lifecycle', 'provider': 'provider', 'terraform_resource_type': 'terraformResourceType', 'terraform_generator_metadata': 'terraformGeneratorMetadata'})
class TerraformResourceConfig(TerraformMetaArguments):
    def __init__(self, *, count: typing.Optional[jsii.Number]=None, depends_on: typing.Optional[typing.List["TerraformResource"]]=None, lifecycle: typing.Optional["TerraformResourceLifecycle"]=None, provider: typing.Optional["TerraformProvider"]=None, terraform_resource_type: str, terraform_generator_metadata: typing.Optional["TerraformGeneratorMetadata"]=None) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param terraform_resource_type: 
        :param terraform_generator_metadata: 

        stability
        :stability: experimental
        """
        if isinstance(lifecycle, dict): lifecycle = TerraformResourceLifecycle(**lifecycle)
        if isinstance(terraform_generator_metadata, dict): terraform_generator_metadata = TerraformGeneratorMetadata(**terraform_generator_metadata)
        self._values = {
            'terraform_resource_type': terraform_resource_type,
        }
        if count is not None: self._values["count"] = count
        if depends_on is not None: self._values["depends_on"] = depends_on
        if lifecycle is not None: self._values["lifecycle"] = lifecycle
        if provider is not None: self._values["provider"] = provider
        if terraform_generator_metadata is not None: self._values["terraform_generator_metadata"] = terraform_generator_metadata

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('count')

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List["TerraformResource"]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('depends_on')

    @builtins.property
    def lifecycle(self) -> typing.Optional["TerraformResourceLifecycle"]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('lifecycle')

    @builtins.property
    def provider(self) -> typing.Optional["TerraformProvider"]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('provider')

    @builtins.property
    def terraform_resource_type(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('terraform_resource_type')

    @builtins.property
    def terraform_generator_metadata(self) -> typing.Optional["TerraformGeneratorMetadata"]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('terraform_generator_metadata')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TerraformResourceConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="cdktf.TerraformResourceLifecycle", jsii_struct_bases=[], name_mapping={'create_before_destroy': 'createBeforeDestroy', 'ignore_changes': 'ignoreChanges', 'prevent_destroy': 'preventDestroy'})
class TerraformResourceLifecycle():
    def __init__(self, *, create_before_destroy: typing.Optional[bool]=None, ignore_changes: typing.Optional[typing.List[str]]=None, prevent_destroy: typing.Optional[bool]=None) -> None:
        """
        :param create_before_destroy: 
        :param ignore_changes: 
        :param prevent_destroy: 

        stability
        :stability: experimental
        """
        self._values = {
        }
        if create_before_destroy is not None: self._values["create_before_destroy"] = create_before_destroy
        if ignore_changes is not None: self._values["ignore_changes"] = ignore_changes
        if prevent_destroy is not None: self._values["prevent_destroy"] = prevent_destroy

    @builtins.property
    def create_before_destroy(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('create_before_destroy')

    @builtins.property
    def ignore_changes(self) -> typing.Optional[typing.List[str]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('ignore_changes')

    @builtins.property
    def prevent_destroy(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('prevent_destroy')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TerraformResourceLifecycle(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class TerraformStack(constructs.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdktf.TerraformStack"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, scope: constructs.Construct, id: str) -> None:
        """
        :param scope: -
        :param id: -

        stability
        :stability: experimental
        """
        jsii.create(TerraformStack, self, [scope, id])

    @jsii.member(jsii_name="addOverride")
    def add_override(self, path: str, value: typing.Any) -> None:
        """
        :param path: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addOverride", [path, value])

    @jsii.member(jsii_name="onSynthesize")
    def on_synthesize(self, session: constructs.ISynthesisSession) -> None:
        """Allows this construct to emit artifacts into the cloud assembly during synthesis.

        This method is usually implemented by framework-level constructs such as ``Stack`` and ``Asset``
        as they participate in synthesizing the cloud assembly.

        :param session: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "onSynthesize", [session])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toTerraform", [])

    @builtins.property
    @jsii.member(jsii_name="artifactFile")
    def artifact_file(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "artifactFile")


class Testing(metaclass=jsii.JSIIMeta, jsii_type="cdktf.Testing"):
    """Testing utilities for cdktf applications.

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="app")
    @builtins.classmethod
    def app(cls) -> "App":
        """Returns an app for testing with the following properties: - Output directory is a temp dir.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "app", [])

    @jsii.member(jsii_name="synth")
    @builtins.classmethod
    def synth(cls, stack: "TerraformStack") -> str:
        """Returns the Terraform synthesized JSON.

        :param stack: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "synth", [stack])


__all__ = [
    "App",
    "AppOptions",
    "BooleanMap",
    "ComplexComputedList",
    "NumberMap",
    "StringMap",
    "TerraformElement",
    "TerraformGeneratorMetadata",
    "TerraformMetaArguments",
    "TerraformModule",
    "TerraformModuleOptions",
    "TerraformOutput",
    "TerraformOutputConfig",
    "TerraformProvider",
    "TerraformProviderConfig",
    "TerraformResource",
    "TerraformResourceConfig",
    "TerraformResourceLifecycle",
    "TerraformStack",
    "Testing",
]

publication.publish()
