from graphene import InputObjectType, String, Field, Int

class Organization_InputField(InputObjectType):
    name = String()
    role = String()
    URL = String()

class OrganismCustomField_InputField(InputObjectType):
    name = String()
    value = String()
    unit = String()
    ontologyTerms = String()

class Material_InputField(InputObjectType):
    text = String()
    ontologyTerms = String()

class Organism_InputField(InputObjectType):
    text = String()
    ontologyTerms = String()

class Sex_InputField(InputObjectType):
    text = String()
    ontologyTerms = String()

class Breed_InputField(InputObjectType):
    text = String()
    ontologyTerms = String()

class BirthDate_InputField(InputObjectType):
    text = String()
    unit = String()

class HealthStatus_InputField(InputObjectType):
    text = String()
    ontologyTerms = String()

class BirthLocationLongitude_InputField(InputObjectType):
    text = String()
    unit = String()

class BirthLocationLatitude_InputField(InputObjectType):
    text = String()
    unit = String()

class BirthWeight_InputField(InputObjectType):
    text = String()
    unit = String()

class PlacentalWeight_InputField(InputObjectType):
    text = String()
    unit = String()

class PregnancyLength_InputField(InputObjectType):
    text = String()
    unit = String()

class PublishedArticles_InputField(InputObjectType):
    articleId = String()
    title = String()
    year = String()
    journal = String()



class OrganismFilterBasic_Argument(InputObjectType):
    biosampleId = String()
    id_number = Int()
    alternativeId = String()
    etag = String()
    name = String()
    description = String()
    releaseDate = String()
    updateDate = String()
    standardMet = String()
    versionLastStandardMet = String()
    project = String()
    secondaryProject = String()
    organization = Field(Organization_InputField)
    customField = Field(OrganismCustomField_InputField)
    material = Field(Material_InputField)
    availability = String()
    organism = Field(Organism_InputField)
    sex = Field(Sex_InputField)
    breed = Field(Breed_InputField)
    birthDate = Field(BirthDate_InputField)
    healthStatus = Field(HealthStatus_InputField)
    birthLocation = String()
    birthLocationLongitude = Field(BirthLocationLongitude_InputField)
    birthLocationLatitude = Field(BirthLocationLatitude_InputField)
    birthWeight = Field(BirthWeight_InputField)
    placentalWeight = Field(PlacentalWeight_InputField)
    pregnancyLength = Field(PregnancyLength_InputField)
    deliveryTiming = String()
    deliveryEase = String()
    childOf = String()
    pedigree = String()
    paperPublished = String()
    publishedArticles = Field(PublishedArticles_InputField)
    

class OrganismFilterJoin_Argument(InputObjectType):
    pass

class OrganismFilter_Argument(InputObjectType):
    basic = Field(OrganismFilterBasic_Argument)
    # join = Field(OrganismFilterJoin_Argument)