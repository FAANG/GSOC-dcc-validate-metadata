from graphene import ObjectType, String

class OrganizationField(ObjectType):
    name = String()
    role = String()
    URL = String()

class CustomFieldField(ObjectType):
    name = String()
    value = String()
    unit = String()
    ontologyTerms = String()

class MaterialField(ObjectType):
    text = String()
    ontologyTerms = String()

class OrganismField(ObjectType):
    text = String()
    ontologyTerms = String()

class SexField(ObjectType):
    text = String()
    ontologyTerms = String()

class BreedField(ObjectType):
    text = String()
    ontologyTerms = String()

class BirthDateField(ObjectType):
    text = String()
    unit = String()

class HealthStatusField(ObjectType):
    text = String()
    ontologyTerms = String()

class BirthLocationLongitudeField(ObjectType):
    text = String()
    unit = String()

class BirthLocationLatitudeField(ObjectType):
    text = String()
    unit = String()

class BirthWeightField(ObjectType):
    text = String()
    unit = String()

class PlacentalWeightField(ObjectType):
    text = String()
    unit = String()

class PregnancyLengthField(ObjectType):
    text = String()
    unit = String()

class PublishedArticlesField(ObjectType):
    articleId = String()
    title = String()
    year = String()
    journal = String()

