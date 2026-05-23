"""
core/management/commands/seed_content.py

Place this file at:
  apps/core/management/__init__.py        (empty file)
  apps/core/management/commands/__init__.py  (empty file)
  apps/core/management/commands/seed_content.py  ← THIS FILE

Run with:
  python manage.py seed_content

What it does:
  - Seeds every section with the exact default text from the original index.html
  - Copies static images from assets/ into media/ so uploaded-image fields work
  - Images/video stay in static/ — media/ references are symlinked so admin can
    later replace them individually without touching static/
"""

import os
import shutil
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings

from apps.core.models import (
    SiteHeader, HeroBanner,
    FeaturesSection, FeatureItem,
    CallToAction,
    ClassesSection, TrainingClass,
    ScheduleSection, ScheduleEntry,
    TrainersSection, Trainer,
    ContactSection, SiteFooter,
)


# ── Helper: copy a file from static/assets/ into media/ and return the relative path ──
def copy_to_media(src_relative: str, dest_relative: str) -> str:
    """
    src_relative  e.g. 'assets/images/first-trainer.jpg'
                  looked up under settings.STATICFILES_DIRS[0]
    dest_relative e.g. 'trainers/first-trainer.jpg'
                  saved under settings.MEDIA_ROOT

    Returns dest_relative on success, or '' on failure.
    """
    static_root = Path(settings.STATICFILES_DIRS[0])
    src  = static_root / src_relative
    dest = Path(settings.MEDIA_ROOT) / dest_relative

    if not src.exists():
        print(f"  [WARN] Static file not found: {src}")
        return ''

    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    return dest_relative


class Command(BaseCommand):
    help = 'Seeds the database with all default content from the original index.html'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.MIGRATE_HEADING('\n▶ Seeding default content...\n'))

        self._seed_header()
        self._seed_hero()
        self._seed_features()
        self._seed_cta()
        self._seed_classes()
        self._seed_schedule()
        self._seed_trainers()
        self._seed_contact()
        self._seed_footer()

        self.stdout.write(self.style.SUCCESS('\n✅ All default content seeded successfully.\n'))

    # ─────────────────────────────────────────────────────────
    # 1. HEADER & NAVIGATION
    # ─────────────────────────────────────────────────────────
    def _seed_header(self):
        SiteHeader.objects.update_or_create(pk=1, defaults={
            'logo_text':          'Training',
            'logo_em_text':       'Studio',
            'logo_url':           '/',
            'nav_home_label':     'Home',
            'nav_about_label':    'About',
            'nav_classes_label':  'Classes',
            'nav_schedules_label':'Schedules',
            'nav_contact_label':  'Contact',
            'nav_signup_label':   'Sign Up',
            'nav_signup_url':     '#',
        })
        self.stdout.write('  ✓ Header')

    # ─────────────────────────────────────────────────────────
    # 2. HERO BANNER
    # Video: copy assets/images/gym-video.mp4 → media/hero/gym-video.mp4
    # ─────────────────────────────────────────────────────────
    def _seed_hero(self):
        video_path = copy_to_media(
            src_relative='assets/images/gym-video.mp4',
            dest_relative='hero/gym-video.mp4',
        )
        HeroBanner.objects.update_or_create(pk=1, defaults={
            'subtitle':         'work harder, get stronger',
            'title_plain':      'easy with our',
            'title_em':         'gym',
            'cta_button_text':  'Become a member',
            'cta_button_url':   '#features',
            'video_file':       video_path,   # '' if the mp4 wasn't found in static/
            'video_url':        '',
        })
        self.stdout.write('  ✓ Hero Banner')

    # ─────────────────────────────────────────────────────────
    # 3. FEATURES SECTION + 6 ITEMS
    # Icon: assets/images/features-first-icon.png (same icon for all 6 in template)
    # ─────────────────────────────────────────────────────────
    def _seed_features(self):
        FeaturesSection.objects.update_or_create(pk=1, defaults={
            'section_title':       'Choose',
            'section_title_em':    'Program',
            'section_description': (
                'Training Studio is free CSS template for gyms and fitness centers. '
                'You are allowed to use this layout for your business website.'
            ),
        })

        icon_path = copy_to_media(
            src_relative='assets/images/features-first-icon.png',
            dest_relative='features/features-first-icon.png',
        )

        items = [
            (
                'Basic Fitness',
                'Please do not re-distribute this template ZIP file on any template '
                'collection website. This is not allowed.',
            ),
            (
                'New Gym Training',
                'If you wish to support TemplateMo website via PayPal, please feel '
                'free to contact us. We appreciate it a lot.',
            ),
            (
                'Basic Muscle Course',
                'Credit goes to Pexels website for images and video background used '
                'in this HTML template.',
            ),
            (
                'Advanced Muscle Course',
                'You may want to browse through Digital Marketing or Corporate HTML '
                'CSS templates on our website.',
            ),
            (
                'Yoga Training',
                'This template is built on Bootstrap v4.3.1 framework. '
                'It is easy to adapt the columns and sections.',
            ),
            (
                'Body Building Course',
                'Suspendisse fringilla et nisi et mattis. Curabitur sed finibus nisi. '
                'Integer nibh sapien, vehicula et auctor.',
            ),
        ]

        for order, (title, desc) in enumerate(items):
            FeatureItem.objects.update_or_create(
                title=title,
                defaults={
                    'icon':        icon_path,
                    'description': desc,
                    'link_text':   'Discover More',
                    'link_url':    '#',
                    'is_active':   True,
                    'order':       order,
                },
            )
        self.stdout.write('  ✓ Features Section + 6 items')

    # ─────────────────────────────────────────────────────────
    # 4. CALL TO ACTION
    # ─────────────────────────────────────────────────────────
    def _seed_cta(self):
        CallToAction.objects.update_or_create(pk=1, defaults={
            'title_part_1':  "Don't",
            'title_em_1':    'think',
            'title_part_2':  ', begin',
            'title_em_2':    'today',
            'title_suffix':  '!',
            'description': (
                'Ut consectetur, metus sit amet aliquet placerat, enim est ultricies ligula, '
                'sit amet dapibus odio augue eget libero. Morbi tempus mauris a nisi luctus imperdiet.'
            ),
            'button_text':   'Become a member',
            'button_url':    '#our-classes',
        })
        self.stdout.write('  ✓ Call To Action')

    # ─────────────────────────────────────────────────────────
    # 5. OUR CLASSES — 4 tabs
    # Images: assets/images/training-image-01..04.jpg
    # Tab icon: assets/images/tabs-first-icon.png
    # ─────────────────────────────────────────────────────────
    def _seed_classes(self):
        ClassesSection.objects.update_or_create(pk=1, defaults={
            'section_title':       'Our',
            'section_title_em':    'Classes',
            'section_description': (
                'Nunc urna sem, laoreet ut metus id, aliquet consequat magna. '
                'Sed viverra ipsum dolor, ultricies fermentum massa consequat eu.'
            ),
            'view_all_text': 'View All Schedules',
            'view_all_url':  '#',
        })

        tab_icon_path = copy_to_media(
            src_relative='assets/images/tabs-first-icon.png',
            dest_relative='classes/tabs/tabs-first-icon.png',
        )

        classes = [
            (
                'First Training Class',
                'training-image-01.jpg',
                'First Training Class',
                (
                    'Phasellus convallis mauris sed elementum vulputate. Donec posuere leo sed dui '
                    'eleifend hendrerit. Sed suscipit suscipit erat, sed vehicula ligula. Aliquam ut '
                    'sem fermentum sem tincidunt lacinia gravida aliquam nunc. Morbi quis erat '
                    'imperdiet, molestie nunc ut, accumsan diam.'
                ),
            ),
            (
                'Second Training Class',
                'training-image-02.jpg',
                'Second Training Class',
                (
                    'Integer dapibus, est vel dapibus mattis, sem mauris luctus leo, ac pulvinar quam '
                    'tortor a velit. Praesent ultrices erat ante, in ultricies augue ultricies faucibus. '
                    'Nam tellus nibh, ullamcorper at mattis non, rhoncus sed massa. Cras quis pulvinar '
                    'eros. Orci varius natoque penatibus et magnis dis parturient montes, nascetur '
                    'ridiculus mus.'
                ),
            ),
            (
                'Third Training Class',
                'training-image-03.jpg',
                'Third Training Class',
                (
                    'Fusce laoreet malesuada rhoncus. Donec ultricies diam tortor, id auctor neque '
                    'posuere sit amet. Aliquam pharetra, augue vel cursus porta, nisi tortor vulputate '
                    'sapien, id scelerisque felis magna id felis. Proin neque metus, pellentesque '
                    'pharetra semper vel, accumsan a neque.'
                ),
            ),
            (
                'Fourth Training Class',
                'training-image-04.jpg',
                'Fourth Training Class',
                (
                    'Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac '
                    'turpis egestas. Aenean ultrices elementum odio ac tempus. Etiam eleifend orci '
                    'lectus, eget venenatis ipsum commodo et.'
                ),
            ),
        ]

        for order, (tab_label, img_file, name, desc) in enumerate(classes):
            image_path = copy_to_media(
                src_relative=f'assets/images/{img_file}',
                dest_relative=f'classes/{img_file}',
            )
            TrainingClass.objects.update_or_create(
                name=name,
                defaults={
                    'tab_label':            tab_label,
                    'tab_icon':             tab_icon_path,
                    'image':                image_path,
                    'image_alt':            name,
                    'description':          desc,
                    'schedule_button_text': 'View Schedule',
                    'schedule_url':         '#',
                    'is_active':            True,
                    'order':                order,
                },
            )
        self.stdout.write('  ✓ Our Classes + 4 tabs')

    # ─────────────────────────────────────────────────────────
    # 6. SCHEDULE — 5 rows
    # Trainers must exist first (seeded in _seed_trainers).
    # We seed trainers before schedule; this method is called after.
    # ─────────────────────────────────────────────────────────
    def _seed_schedule(self):
        ScheduleSection.objects.update_or_create(pk=1, defaults={
            'section_title':       'Classes',
            'section_title_em':    'Schedule',
            'section_description': (
                'Nunc urna sem, laoreet ut metus id, aliquet consequat magna. '
                'Sed viverra ipsum dolor, ultricies fermentum massa consequat eu.'
            ),
        })
        self.stdout.write('  ✓ Schedule Section heading')
        # Rows are seeded in _seed_schedule_rows() called after trainers exist.

    def _seed_schedule_rows(self):
        """Called after trainers are seeded so FK lookups work."""
        def get_trainer(name):
            return Trainer.objects.filter(name=name).first()

        rows = [
            # (class_name, slot1_day, slot1_time, slot2_day, slot2_time, trainer_name)
            ('Fitness Class',      'monday',    '10:00AM - 11:30AM', 'tuesday',   '2:00PM - 3:30PM',  'William G. Stewart'),
            ('Muscle Training',    'friday',    '10:00AM - 11:30AM', 'thursday',  '2:00PM - 3:30PM',  'Paul D. Newman'),
            ('Body Building',      'tuesday',   '10:00AM - 11:30AM', 'monday',    '2:00PM - 3:30PM',  'Boyd C. Harris'),
            ('Yoga Training Class','wednesday', '10:00AM - 11:30AM', 'friday',    '2:00PM - 3:30PM',  'Hector T. Daigle'),
            ('Advanced Training',  'thursday',  '10:00AM - 11:30AM', 'wednesday', '2:00PM - 3:30PM',  'Bret D. Bowers'),
        ]

        for order, (cname, d1, t1, d2, t2, tname) in enumerate(rows):
            ScheduleEntry.objects.update_or_create(
                class_name=cname,
                defaults={
                    'slot_1_day':  d1,
                    'slot_1_time': t1,
                    'slot_2_day':  d2,
                    'slot_2_time': t2,
                    'trainer':     get_trainer(tname),
                    'is_active':   True,
                    'order':       order,
                },
            )
        self.stdout.write('  ✓ Schedule rows (5 entries)')

    # ─────────────────────────────────────────────────────────
    # 7. TRAINERS — 3 cards
    # Images: assets/images/first-trainer.jpg etc.
    # ─────────────────────────────────────────────────────────
    def _seed_trainers(self):
        TrainersSection.objects.update_or_create(pk=1, defaults={
            'section_title':       'Expert',
            'section_title_em':    'Trainers',
            'section_description': (
                'Nunc urna sem, laoreet ut metus id, aliquet consequat magna. '
                'Sed viverra ipsum dolor, ultricies fermentum massa consequat eu.'
            ),
        })

        trainers = [
            (
                'Bret D. Bowers',
                'Strength Trainer',
                'first-trainer.jpg',
                'Bitters cliche tattooed 8-bit distillery mustache. Keytar succulents '
                'gluten-free vegan church-key pour-over seitan flannel.',
            ),
            (
                'Hector T. Daigle',
                'Muscle Trainer',
                'second-trainer.jpg',
                'Bitters cliche tattooed 8-bit distillery mustache. Keytar succulents '
                'gluten-free vegan church-key pour-over seitan flannel.',
            ),
            (
                'Paul D. Newman',
                'Power Trainer',
                'third-trainer.jpg',
                'Bitters cliche tattooed 8-bit distillery mustache. Keytar succulents '
                'gluten-free vegan church-key pour-over seitan flannel.',
            ),
        ]

        for order, (name, specialty, img_file, bio) in enumerate(trainers):
            photo_path = copy_to_media(
                src_relative=f'assets/images/{img_file}',
                dest_relative=f'trainers/{img_file}',
            )
            Trainer.objects.update_or_create(
                name=name,
                defaults={
                    'specialty':    specialty,
                    'photo':        photo_path,
                    'photo_alt':    name,
                    'bio':          bio,
                    'facebook_url': '#',
                    'twitter_url':  '#',
                    'linkedin_url': '#',
                    'behance_url':  '#',
                    'is_active':    True,
                    'order':        order,
                },
            )

        self.stdout.write('  ✓ Trainers Section + 3 trainers')

        # Now seed schedule rows (trainers must exist first for FK)
        self._seed_schedule_rows()

    # ─────────────────────────────────────────────────────────
    # 8. CONTACT SECTION
    # Google Maps embed URL taken directly from the original iframe src
    # ─────────────────────────────────────────────────────────
    def _seed_contact(self):
        ContactSection.objects.update_or_create(pk=1, defaults={
            'google_maps_embed_url': (
                'https://maps.google.com/maps?q=Av.+L%C3%BAcio+Costa,'
                '+Rio+de+Janeiro+-+RJ,+Brazil&t=&z=13&ie=UTF8&iwloc=&output=embed'
            ),
            'map_height': 600,
        })
        self.stdout.write('  ✓ Contact Section (Google Maps)')

    # ─────────────────────────────────────────────────────────
    # 9. FOOTER
    # ─────────────────────────────────────────────────────────
    def _seed_footer(self):
        SiteFooter.objects.update_or_create(pk=1, defaults={
            'copyright_text':      'Copyright © 2020 Training Studio - Designed by TemplateMo. Distributed by ThemeWagon',
            'show_designer_credit': True,
        })
        self.stdout.write('  ✓ Footer')