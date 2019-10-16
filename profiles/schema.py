import graphene
from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models import CharField, Value
from django.db.models.functions import Concat
from django.utils.translation import override
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from munigeo.models import AdministrativeDivision
from thesaurus.models import Concept


from .models import BasicProfile


class ConceptType(DjangoObjectType):
    class Meta:
        model = Concept
        fields = ("code",)

    vocabulary = graphene.String()
    label = graphene.String()

    def resolve_vocabulary(self, info, **kwargs):
        return self.vocabulary.prefix


class AdministrativeDivisionType(DjangoObjectType):
    class Meta:
        model = AdministrativeDivision
        fields = ("children", "origin_id", "ocd_id", "municipality")

    type = graphene.String()
    name = graphene.String()

    def resolve_children(self, info, **kwargs):
        return self.children.filter(type__type="sub_district")

    def resolve_type(self, info, **kwargs):
        return self.type.type


with override("en"):
    Language = graphene.Enum(
        "Language", [(l[1].upper(), l[0]) for l in settings.LANGUAGES]
    )
    ContactMethod = graphene.Enum(
        "ContactMethod", [(cm[1].upper(), cm[0]) for cm in settings.CONTACT_METHODS]
    )


class BasicProfileType(DjangoObjectType):
    class Meta:
        model = BasicProfile
        exclude = ("user",)

    language = Language()
    contact_method = ContactMethod()
    concepts_of_interest = graphene.List(ConceptType)
    divisions_of_interest = graphene.List(AdministrativeDivisionType)

    def resolve_concepts_of_interest(self, info, **kwargs):
        return self.concepts_of_interest.all()

    def resolve_divisions_of_interest(self, info, **kwargs):
        return self.divisions_of_interest.all()


class BasicProfileInput(graphene.InputObjectType):
    nickname = graphene.String()
    image = graphene.String()
    email = graphene.String()
    phone = graphene.String()
    language = Language()
    contact_method = ContactMethod()
    concepts_of_interest = graphene.List(graphene.String)
    divisions_of_interest = graphene.List(graphene.String)


class UpdateBasicProfile(graphene.Mutation):
    class Arguments:
        profile = BasicProfileInput(required=True)

    profile = graphene.Field(BasicProfileType)

    @login_required
    def mutate(self, info, **kwargs):
        profile_data = kwargs.pop("profile")
        concepts_of_interest = profile_data.pop("concepts_of_interest", [])
        divisions_of_interest = profile_data.pop("divisions_of_interest", [])
        profile, created = BasicProfile.objects.get_or_create(user=info.context.user)
        for field, value in profile_data.items():
            setattr(profile, field, value)
        profile.save()

        cois = Concept.objects.annotate(
            identifier=Concat(
                "vocabulary__prefix", Value(":"), "code", output_field=CharField()
            )
        ).filter(identifier__in=concepts_of_interest)
        profile.concepts_of_interest.set(cois)
        ads = AdministrativeDivision.objects.filter(ocd_id__in=divisions_of_interest)
        profile.divisions_of_interest.set(ads)

        return UpdateBasicProfile(profile=profile)


class Query(graphene.ObjectType):
    profile = graphene.Field(BasicProfileType)
    concepts_of_interest = graphene.List(ConceptType)
    divisions_of_interest = graphene.List(AdministrativeDivisionType)

    @login_required
    def resolve_profile(self, info, **kwargs):
        return (
            BasicProfile.objects.filter(user=info.context.user)
            .prefetch_related("concepts_of_interest", "divisions_of_interest")
            .first()
        )

    def resolve_concepts_of_interest(self, info, **kwargs):
        return Concept.objects.all()

    def resolve_divisions_of_interest(self, info, **kwargs):
        return AdministrativeDivision.objects.filter(division_of_interest__isnull=False)


class Mutation(graphene.ObjectType):
    update_profile = UpdateBasicProfile.Field()
