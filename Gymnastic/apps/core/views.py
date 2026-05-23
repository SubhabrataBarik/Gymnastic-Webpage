from django.shortcuts import render
from .models import (
    SiteHeader, HeroBanner, FeaturesSection, FeatureItem,
    CallToAction, ClassesSection, TrainingClass,
    ScheduleSection, ScheduleEntry, TrainersSection,
    Trainer, ContactSection, SiteFooter
)

def homepage(request):
    context = {
        'header':            SiteHeader.get_solo(),
        'hero':              HeroBanner.get_solo(),
        'features':          FeaturesSection.get_solo(),
        'feature_items':     FeatureItem.objects.filter(is_active=True),
        'cta':               CallToAction.get_solo(),
        'classes_section':   ClassesSection.get_solo(),
        'training_classes':  TrainingClass.objects.filter(is_active=True),
        'schedule_section':  ScheduleSection.get_solo(),
        'schedule_entries':  ScheduleEntry.objects.filter(is_active=True)
                                          .select_related('trainer'),
        'trainers_section':  TrainersSection.get_solo(),
        'trainers':          Trainer.objects.filter(is_active=True),
        'contact':           ContactSection.get_solo(),
        'footer':            SiteFooter.get_solo(),
    }
    return render(request, 'index.html', context)