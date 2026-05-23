from rest_framework import serializers
from .models import *


class SiteHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteHeader
        fields = '__all__'

class HeroBannerSerializer(serializers.ModelSerializer):
    video_source = serializers.ReadOnlyField()
    class Meta:
        model = HeroBanner
        fields = '__all__'

class FeaturesSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturesSection
        fields = '__all__'

class FeatureItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureItem
        fields = '__all__'

class CallToActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallToAction
        fields = '__all__'

class ClassesSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassesSection
        fields = '__all__'

class TrainingClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingClass
        fields = '__all__'

class ScheduleSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleSection
        fields = '__all__'

class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = '__all__'

class ScheduleEntrySerializer(serializers.ModelSerializer):
    trainer_name = serializers.CharField(source='trainer.name', read_only=True)
    class Meta:
        model = ScheduleEntry
        fields = '__all__'

class TrainersSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainersSection
        fields = '__all__'

class ContactSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSection
        fields = '__all__'

class SiteFooterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteFooter
        fields = '__all__'


# ── Mega serializer: entire page in one API call ──
class FullPageSerializer(serializers.Serializer):
    header          = SiteHeaderSerializer()
    hero            = HeroBannerSerializer()
    features        = FeaturesSectionSerializer()
    feature_items   = FeatureItemSerializer(many=True)
    cta             = CallToActionSerializer()
    classes_section = ClassesSectionSerializer()
    training_classes = TrainingClassSerializer(many=True)
    schedule_section = ScheduleSectionSerializer()
    schedule_entries = ScheduleEntrySerializer(many=True)
    trainers_section = TrainersSectionSerializer()
    trainers         = TrainerSerializer(many=True)
    contact          = ContactSectionSerializer()
    footer           = SiteFooterSerializer()