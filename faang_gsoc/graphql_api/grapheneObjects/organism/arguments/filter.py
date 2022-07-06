from graphene import InputObjectType, String, Field, Int, List

class OrganismOrganization_InputField(InputObjectType):
    name = List(String)
    role = List(String)
    URL = List(String)

class OrganismCustomField_InputField(InputObjectType):
    name = List(String)
    value = List(String)
    unit = List(String)
    ontologyTerms = List(String)

class Material_InputField(InputObjectType):
    text = List(String)
    ontologyTerms = List(String)

class Organism_InputField(InputObjectType):
    text = List(String)
    ontologyTerms = List(String)

class Sex_InputField(InputObjectType):
    text = List(String)
    ontologyTerms = List(String)

class Breed_InputField(InputObjectType):
    text = List(String)
    ontologyTerms = List(String)

class BirthDate_InputField(InputObjectType):
    text = List(String)
    unit = List(String)

class HealthStatus_InputField(InputObjectType):
    text = List(String)
    ontologyTerms = List(String)

class BirthLocationLongitude_InputField(InputObjectType):
    text = List(String)
    unit = List(String)

class BirthLocationLatitude_InputField(InputObjectType):
    text = List(String)
    unit = List(String)

class BirthWeight_InputField(InputObjectType):
    text = List(String)
    unit = List(String)

class PlacentalWeight_InputField(InputObjectType):
    text = List(String)
    unit = List(String)

class PregnancyLength_InputField(InputObjectType):
    text = List(String)
    unit = List(String)

class OrganismPublishedArticles_InputField(InputObjectType):
    articleId = List(String)
    title = List(String)
    year = List(String)
    journal = List(String)



class OrganismFilterBasic_Argument(InputObjectType):
    biosampleId = List(String)
    id_number = List(Int)
    alternativeId = List(String)
    etag = List(String)
    name = List(String)
    description = List(String)
    releaseDate = List(String)
    updateDate = List(String)
    standardMet = List(String)
    versionLastStandardMet = List(String)
    project = List(String)
    secondaryProject = List(String)
    organization = Field(OrganismOrganization_InputField)
    customField = Field(OrganismCustomField_InputField)
    material = Field(Material_InputField)
    availability = List(String)
    organism = Field(Organism_InputField)
    sex = Field(Sex_InputField)
    breed = Field(Breed_InputField)
    birthDate = Field(BirthDate_InputField)
    healthStatus = Field(HealthStatus_InputField)
    birthLocation = List(String)
    birthLocationLongitude = Field(BirthLocationLongitude_InputField)
    birthLocationLatitude = Field(BirthLocationLatitude_InputField)
    birthWeight = Field(BirthWeight_InputField)
    placentalWeight = Field(PlacentalWeight_InputField)
    pregnancyLength = Field(PregnancyLength_InputField)
    deliveryTiming = List(String)
    deliveryEase = List(String)
    childOf = List(String)
    pedigree = List(String)
    paperPublished = List(String)
    publishedArticles = Field(OrganismPublishedArticles_InputField)
    

class OrganismFilterJoin_Argument(InputObjectType):
    file = Field('graphql_api.grapheneObjects.file.arguments.filter.FileFilter_Argument')
    specimen = Field('graphql_api.grapheneObjects.specimen.arguments.filter.SpecimenFilter_Argument')
    protocol_samples = Field('graphql_api.grapheneObjects.protocol_samples.arguments.filter.ProtocolSamplesFilter_Argument')


class OrganismFilter_Argument(InputObjectType):
    basic = Field(OrganismFilterBasic_Argument)
    join = Field(OrganismFilterJoin_Argument)