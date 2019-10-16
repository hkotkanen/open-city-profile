import graphene
from django.conf import settings
from django.db.models import CharField, Value
from django.db.models.functions import Concat
from django.utils.translation import override
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from .models import DataUseConsent, DataUseConsentPurpose


class DataUseConsentPurposeType(DjangoObjectType):
    class Meta:
        model = DataUseConsentPurpose


class DataUseConsentType(DjangoObjectType):
    class Meta:
        model = DataUseConsent
        fields = (
            "uuid",
            "issued_at",
            "modified_at",
            "expires_at",
            "content_type",
            "object_id",
            "purpose"
        )

    audience = graphene.String()
    consenter = graphene.String()
    content_type = graphene.String()

    def resolve_audience(self, info, **kwargs):
        return str(self.audience)

    def resolve_consenter(self, info, **kwargs):
        return str(self.consenter)

    def resolve_content_type(self, info, **kwargs):
        return str(self.content_type)


class DataUseConsentInput(graphene.InputObjectType):
    purpose_id = graphene.ID()
    audience = graphene.String()
    phone = graphene.String()
    concepts_of_interest = graphene.List(graphene.String)
    divisions_of_interest = graphene.List(graphene.String)


class CreateDataUseConsent(graphene.Mutation):
    class Arguments:
        consent_data = DataUseConsentInput(required=True)
        consenter_user_id = graphene.ID()

    data_use_consent = graphene.Field(DataUseConsentType)

    @login_required
    def mutate(self, info, **kwargs):
        pass
        # profile_data = kwargs.pop("profile")
        # concepts_of_interest = profile_data.pop("concepts_of_interest", [])
        # divisions_of_interest = profile_data.pop("divisions_of_interest", [])
        # profile, created = BasicProfile.objects.get_or_create(user=info.context.user)
        # for field, value in profile_data.items():
        #     setattr(profile, field, value)
        # profile.save()
        #
        # cois = Concept.objects.annotate(
        #     identifier=Concat(
        #         "vocabulary__prefix", Value(":"), "code", output_field=CharField()
        #     )
        # ).filter(identifier__in=concepts_of_interest)
        # profile.concepts_of_interest.set(cois)
        # ads = AdministrativeDivision.objects.filter(ocd_id__in=divisions_of_interest)
        # profile.divisions_of_interest.set(ads)
        #
        # return CreateDataUseConsent(profile=profile)


class Query(graphene.ObjectType):
    consents = graphene.List(DataUseConsentType)
    consent_purposes = graphene.List(DataUseConsentPurposeType)

    @login_required
    def resolve_consents(self, info, **kwargs):
        return DataUseConsent.objects.filter(consenter=info.context.user)

    def resolve_consent_purposes(self, info, **kwargs):
        return DataUseConsentPurpose.objects.all()


# class Mutation(graphene.ObjectType):
#     create_data_use_consent = CreateDataUseConsent.Field()
