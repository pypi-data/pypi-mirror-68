import inspect

from marshmallow import Schema, SchemaOpts, post_load, fields
from marshmallow.schema import SchemaMeta
from marshmallow_enum import EnumField

from marshmallow_pynamodb.convert import attribute2field
from marshmallow_pynamodb.fields import PynamoNested
from pynamodb.attributes import Attribute
from six import iteritems


class ModelOpts(SchemaOpts):
    def __init__(self, meta, **kwargs):
        SchemaOpts.__init__(self, meta, **kwargs)
        self.model = getattr(meta, "model", None)
        self.inherit_field_models = getattr(meta, "inherit_field_models", False)


class ModelMeta(SchemaMeta):
    @classmethod
    def get_declared_fields(mcs, klass, cls_fields, inherited_fields, dict_cls):
        """Get Declared Fields."""
        declared_fields = super(ModelMeta, mcs).get_declared_fields(
            klass, cls_fields or [], inherited_fields or [], dict_cls
        )
        if klass.opts.model:
            if not getattr(klass.opts, "inherit_field_models", False):
                model_list = [klass.opts.model]
            else:
                model_list = [
                    pynamo_model for pynamo_model in inspect.getmro(klass.opts.model)
                ][:-1]
            for model in model_list:
                attributes = {
                    name: attr
                    for name, attr in iteritems(vars(model))
                    if isinstance(attr, Attribute)
                }
                model.attributes = dict()
                for attr_name, attribute in iteritems(attributes):
                    if declared_fields.get(attr_name):
                        continue

                    field = attribute2field(attribute)

                    if field == PynamoNested:
                        instance_of = type(attribute)

                        class Meta:
                            model = instance_of

                        sub_model = type(
                            instance_of.__name__, (ModelSchema,), {"Meta": Meta}
                        )
                        field = field(sub_model)
                    elif field == fields.List:

                        class Meta:
                            model = attribute.element_type

                        element_type = type(
                            attribute.element_type.__name__,
                            (ModelSchema,),
                            {"Meta": Meta},
                        )
                        field = field(PynamoNested(element_type))
                    elif field == EnumField:
                        field = field(attribute.enum_type, by_value=True)
                    else:
                        field = field()

                    field_name = (
                        attribute.attr_name if attribute.attr_name else attr_name
                    )
                    if (
                        attribute.is_hash_key
                        or attribute.is_range_key
                        or not attribute.null
                    ):
                        field.required = True
                        if attribute.is_hash_key:
                            klass.opts.hash_key = field_name
                        elif attribute.is_range_key:
                            klass.opts.range_key = field_name

                    # The `default` argument in PynamoDB
                    # is equivalent to `missing` argument in Marshmallow
                    # Example: for a UTCDateTimeAttribute, default value
                    # must be a datetime object:
                    # Datetime obj (from Pynamo default) -> String (DynamoDB)
                    # Payload Input (Json) -> Datetime obj (from Marshmallow missing) -> String (DynamoDB)
                    field.missing = attribute.default
                    declared_fields[field_name] = field
        return declared_fields


class ModelSchema(Schema, metaclass=ModelMeta):
    OPTIONS_CLASS = ModelOpts

    @post_load
    def hydrate_pynamo_model(self, data, **kwargs):
        """Hydrate PynamoDB Model."""
        hash_key = data.pop(getattr(self.opts, "hash_key", None), None)
        range_key = data.pop(getattr(self.opts, "range_key", None), None)

        if hash_key or range_key:  # this is Model
            return self.opts.model(hash_key=hash_key, range_key=range_key, **data)
        else:  # this is a MapAttribute
            return self.opts.model(**data)
