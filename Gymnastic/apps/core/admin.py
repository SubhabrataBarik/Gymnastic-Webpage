"""
apps/core/admin.py

Full Django Admin configuration for all core models.
"""

from django.contrib import admin
from django.utils.html import format_html
from solo.admin import SingletonModelAdmin
from ordered_model.admin import OrderedModelAdmin

from .models import (
    SiteHeader, HeroBanner,
    FeaturesSection, FeatureItem,
    CallToAction,
    ClassesSection, TrainingClass,
    ScheduleSection, ScheduleEntry,
    TrainersSection, Trainer,
    ContactSection, SiteFooter,
)


# ═══════════════════════════════════════════════════════════
# SINGLETON MODELS
# django-solo gives each one a single-object edit page
# ═══════════════════════════════════════════════════════════

@admin.register(SiteHeader)
class SiteHeaderAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Logo', {
            'fields': ('logo_text', 'logo_em_text', 'logo_url'),
        }),
        ('Navigation Labels', {
            'fields': (
                'nav_home_label', 'nav_about_label', 'nav_classes_label',
                'nav_schedules_label', 'nav_contact_label',
            ),
        }),
        ('Sign Up Button', {
            'fields': ('nav_signup_label', 'nav_signup_url'),
        }),
    )


@admin.register(HeroBanner)
class HeroBannerAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Headline Text', {
            'fields': ('subtitle', 'title_plain', 'title_em'),
        }),
        ('CTA Button', {
            'fields': ('cta_button_text', 'cta_button_url'),
        }),
        ('Background Video', {
            'description': 'Upload an MP4 file OR paste an external URL. Uploaded file takes priority.',
            'fields': ('video_file', 'video_url'),
        }),
    )


@admin.register(FeaturesSection)
class FeaturesSectionAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Section Heading', {
            'fields': ('section_title', 'section_title_em', 'section_description'),
        }),
    )


@admin.register(CallToAction)
class CallToActionAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Headline', {
            'description': 'Renders as: [part1] <em>[em1]</em>[part2] <em>[em2]</em>[suffix]',
            'fields': ('title_part_1', 'title_em_1', 'title_part_2', 'title_em_2', 'title_suffix'),
        }),
        ('Body & Button', {
            'fields': ('description', 'button_text', 'button_url'),
        }),
    )


@admin.register(ClassesSection)
class ClassesSectionAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Section Heading', {
            'fields': ('section_title', 'section_title_em', 'section_description'),
        }),
        ('"View All" Button', {
            'fields': ('view_all_text', 'view_all_url'),
        }),
    )


@admin.register(ScheduleSection)
class ScheduleSectionAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Section Heading', {
            'fields': ('section_title', 'section_title_em', 'section_description'),
        }),
    )


@admin.register(TrainersSection)
class TrainersSectionAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Section Heading', {
            'fields': ('section_title', 'section_title_em', 'section_description'),
        }),
    )


@admin.register(ContactSection)
class ContactSectionAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Google Maps', {
            'description': (
                'Go to Google Maps → Search your location → Share → '
                'Embed a map → Copy only the src="..." URL and paste it below.'
            ),
            'fields': ('google_maps_embed_url', 'map_height'),
        }),
    )


@admin.register(SiteFooter)
class SiteFooterAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Footer Text', {
            'fields': ('copyright_text', 'show_designer_credit'),
        }),
    )


# ═══════════════════════════════════════════════════════════
# LIST MODELS (ordered, with image previews)
# ═══════════════════════════════════════════════════════════

@admin.register(FeatureItem)
class FeatureItemAdmin(OrderedModelAdmin):
    list_display    = ('order', 'icon_preview', 'title', 'is_active', 'move_up_down_links')
    list_display_links = ('title',)
    list_editable   = ('is_active',)
    search_fields   = ('title', 'description')
    ordering        = ('order',)

    fieldsets = (
        ('Content', {
            'fields': ('title', 'description'),
        }),
        ('Icon', {
            'fields': ('icon',),
        }),
        ('Link', {
            'fields': ('link_text', 'link_url'),
        }),
        ('Visibility', {
            'fields': ('is_active',),
        }),
    )

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" height="40" />', obj.icon.url)
        return '—'
    icon_preview.short_description = 'Icon'


@admin.register(TrainingClass)
class TrainingClassAdmin(OrderedModelAdmin):
    list_display    = ('order', 'image_preview', 'name', 'tab_label', 'is_active', 'move_up_down_links')
    list_display_links = ('name',)
    list_editable   = ('is_active',)
    ordering        = ('order',)

    fieldsets = (
        ('Tab', {
            'fields': ('tab_label', 'tab_icon'),
        }),
        ('Content Panel', {
            'fields': ('name', 'image', 'image_alt', 'description'),
        }),
        ('Button', {
            'fields': ('schedule_button_text', 'schedule_url'),
        }),
        ('Visibility', {
            'fields': ('is_active',),
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="50" />', obj.image.url)
        return '—'
    image_preview.short_description = 'Image'


@admin.register(Trainer)
class TrainerAdmin(OrderedModelAdmin):
    list_display    = ('order', 'photo_preview', 'name', 'specialty', 'is_active', 'move_up_down_links')
    list_display_links = ('name',)
    list_editable   = ('is_active',)
    search_fields   = ('name', 'specialty')
    ordering        = ('order',)

    fieldsets = (
        ('Profile', {
            'fields': ('name', 'specialty', 'photo', 'photo_alt', 'bio'),
        }),
        ('Social Links', {
            'description': 'Leave blank to hide the icon.',
            'fields': ('facebook_url', 'twitter_url', 'linkedin_url', 'behance_url'),
            'classes': ('collapse',),
        }),
        ('Visibility', {
            'fields': ('is_active',),
        }),
    )

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" height="50" style="border-radius:50%"/>', obj.photo.url)
        return '—'
    photo_preview.short_description = 'Photo'


@admin.register(ScheduleEntry)
class ScheduleEntryAdmin(OrderedModelAdmin):
    list_display    = (
        'order', 'class_name',
        'slot_1_day', 'slot_1_time',
        'slot_2_day', 'slot_2_time',
        'trainer', 'is_active', 'move_up_down_links',
    )
    list_display_links = ('class_name',)
    list_editable   = ('is_active',)
    list_filter     = ('slot_1_day', 'slot_2_day', 'trainer', 'is_active')
    search_fields   = ('class_name', 'trainer__name')
    autocomplete_fields = ('trainer',)
    ordering        = ('order',)

    fieldsets = (
        ('Class', {
            'fields': ('class_name', 'trainer'),
        }),
        ('Slot 1', {
            'fields': ('slot_1_day', 'slot_1_time'),
        }),
        ('Slot 2', {
            'fields': ('slot_2_day', 'slot_2_time'),
        }),
        ('Visibility', {
            'fields': ('is_active',),
        }),
    )