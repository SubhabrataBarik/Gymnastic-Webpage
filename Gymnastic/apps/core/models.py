from django.db import models
from solo.models import SingletonModel
from ordered_model.models import OrderedModel


# ─────────────────────────────────────────────
# HEADER / NAVIGATION
# ─────────────────────────────────────────────

class SiteHeader(SingletonModel):
    """
    Controls: Logo text, nav link labels and their #anchor targets,
    and the Sign Up button URL.
    HTML equivalent: <a class="logo">, <ul class="nav">
    """
    logo_text       = models.CharField(max_length=100, default="Training")
    logo_em_text    = models.CharField(max_length=100, default="Studio",
                          help_text="Italic part of the logo (inside <em> tag)")
    logo_url        = models.CharField(max_length=200, default="index.html")

    # Nav labels — anchors are fixed in template but labels are editable
    nav_home_label      = models.CharField(max_length=50, default="Home")
    nav_about_label     = models.CharField(max_length=50, default="About")
    nav_classes_label   = models.CharField(max_length=50, default="Classes")
    nav_schedules_label = models.CharField(max_length=50, default="Schedules")
    nav_contact_label   = models.CharField(max_length=50, default="Contact")
    nav_signup_label    = models.CharField(max_length=50, default="Sign Up")
    nav_signup_url      = models.CharField(max_length=200, default="#",
                          help_text="URL for the Sign Up button in the nav")

    class Meta:
        verbose_name = "Site Header & Navigation"

    def __str__(self):
        return "Site Header & Navigation"


# ─────────────────────────────────────────────
# HERO / MAIN BANNER
# ─────────────────────────────────────────────

class HeroBanner(SingletonModel):
    """
    Controls: Video background, subtitle (h6), headline (h2 + em), CTA button.
    HTML equivalent: <div class="main-banner"> / <div class="caption">
    """
    subtitle        = models.CharField(max_length=200, default="work harder, get stronger",
                          help_text="Small text above the main headline (h6)")
    title_plain     = models.CharField(max_length=200, default="easy with our",
                          help_text="Plain part of the main headline (h2)")
    title_em        = models.CharField(max_length=100, default="gym",
                          help_text="Italic/highlighted part of the main headline (<em>)")
    cta_button_text = models.CharField(max_length=100, default="Become a member")
    cta_button_url  = models.CharField(max_length=200, default="#features")

    # Video — store the file path or a URL
    video_file      = models.FileField(upload_to='hero/', blank=True,
                          help_text="Upload a .mp4 video for the banner background")
    video_url       = models.URLField(blank=True,
                          help_text="OR enter an external video URL (used if no file uploaded)")

    class Meta:
        verbose_name = "Hero Banner"

    def __str__(self):
        return "Hero Banner"

    @property
    def video_source(self):
        if self.video_file:
            return self.video_file.url
        return self.video_url


# ─────────────────────────────────────────────
# FEATURES SECTION
# ─────────────────────────────────────────────

class FeaturesSection(SingletonModel):
    """
    Controls the heading of the #features section.
    HTML equivalent: <section id="features"> .section-heading
    """
    section_title       = models.CharField(max_length=100, default="Choose")
    section_title_em    = models.CharField(max_length=100, default="Program",
                              help_text="Italic/highlighted word in section heading (<em>)")
    section_description = models.TextField(
        default="Training Studio is free CSS template for gyms and fitness centers.")

    class Meta:
        verbose_name = "Features Section Heading"

    def __str__(self):
        return "Features Section Heading"


class FeatureItem(OrderedModel):
    """
    One program feature card. There are 6 in the original template.
    HTML equivalent: <li class="feature-item"> inside <ul class="features-items">
    """
    icon            = models.ImageField(upload_to='features/', blank=True,
                          help_text="Icon image shown on the left of the card")
    title           = models.CharField(max_length=150,
                          help_text="e.g. 'Basic Fitness', 'Yoga Training'")
    description     = models.TextField()
    link_text       = models.CharField(max_length=100, default="Discover More")
    link_url        = models.CharField(max_length=200, default="#")
    is_active       = models.BooleanField(default=True)

    order_with_respect_to = None  # global ordering

    class Meta(OrderedModel.Meta):
        verbose_name = "Feature Item"
        verbose_name_plural = "Feature Items"

    def __str__(self):
        return self.title


# ─────────────────────────────────────────────
# CALL TO ACTION
# ─────────────────────────────────────────────

class CallToAction(SingletonModel):
    """
    The full-width CTA strip between Features and Classes.
    HTML equivalent: <section id="call-to-action">
    Original headline: Don't <em>think</em>, begin <em>today</em>!
    """
    title_part_1    = models.CharField(max_length=100, default="Don't",
                          help_text="Plain text before first <em>")
    title_em_1      = models.CharField(max_length=100, default="think",
                          help_text="First italic word")
    title_part_2    = models.CharField(max_length=100, default=", begin",
                          help_text="Plain text between the two <em> tags")
    title_em_2      = models.CharField(max_length=100, default="today",
                          help_text="Second italic word")
    title_suffix    = models.CharField(max_length=10, default="!",
                          help_text="Any trailing character (e.g. '!')")
    description     = models.TextField(
        default="Ut consectetur, metus sit amet aliquet placerat...")
    button_text     = models.CharField(max_length=100, default="Become a member")
    button_url      = models.CharField(max_length=200, default="#our-classes")

    class Meta:
        verbose_name = "Call to Action Section"

    def __str__(self):
        return "Call to Action Section"


# ─────────────────────────────────────────────
# OUR CLASSES
# ─────────────────────────────────────────────

class ClassesSection(SingletonModel):
    """
    Controls the heading of the #our-classes section.
    HTML equivalent: <section id="our-classes"> .section-heading
    """
    section_title       = models.CharField(max_length=100, default="Our")
    section_title_em    = models.CharField(max_length=100, default="Classes")
    section_description = models.TextField(
        default="Nunc urna sem, laoreet ut metus id...")
    view_all_text       = models.CharField(max_length=100, default="View All Schedules")
    view_all_url        = models.CharField(max_length=200, default="#")

    class Meta:
        verbose_name = "Classes Section Heading"

    def __str__(self):
        return "Classes Section Heading"


class TrainingClass(OrderedModel):
    """
    One tab in the #our-classes tabbed section. 4 items in original template.
    HTML equivalent: <li><a href="#tabs-N"> and <article id="tabs-N">
    """
    tab_label       = models.CharField(max_length=150,
                          help_text="Label in the left-side tab list, e.g. 'First Training Class'")
    tab_icon        = models.ImageField(upload_to='classes/tabs/', blank=True)
    name            = models.CharField(max_length=150,
                          help_text="Heading inside the tab content panel (h4)")
    image           = models.ImageField(upload_to='classes/',
                          help_text="Image shown in the class content panel")
    image_alt       = models.CharField(max_length=200, blank=True)
    description     = models.TextField()
    schedule_button_text = models.CharField(max_length=100, default="View Schedule")
    schedule_url    = models.CharField(max_length=200, default="#")
    is_active       = models.BooleanField(default=True)

    order_with_respect_to = None

    class Meta(OrderedModel.Meta):
        verbose_name = "Training Class"
        verbose_name_plural = "Training Classes"

    def __str__(self):
        return self.name


# ─────────────────────────────────────────────
# SCHEDULE
# ─────────────────────────────────────────────

DAY_CHOICES = [
    ('monday',    'Monday'),
    ('tuesday',   'Tuesday'),
    ('wednesday', 'Wednesday'),
    ('thursday',  'Thursday'),
    ('friday',    'Friday'),
    ('saturday',  'Saturday'),
    ('sunday',    'Sunday'),
]


class ScheduleSection(SingletonModel):
    """
    Controls the heading of the #schedule section.
    HTML equivalent: <section id="schedule"> .section-heading
    """
    section_title       = models.CharField(max_length=100, default="Classes")
    section_title_em    = models.CharField(max_length=100, default="Schedule")
    section_description = models.TextField(
        default="Nunc urna sem, laoreet ut metus id...")

    class Meta:
        verbose_name = "Schedule Section Heading"

    def __str__(self):
        return "Schedule Section Heading"


class ScheduleEntry(OrderedModel):
    """
    One row in the schedule table.
    HTML equivalent: <tr> inside <tbody> in <section id="schedule">

    Each entry has a class name, two time slots on specific days, and a trainer.
    The frontend uses data-tsmeta attributes to filter by day.
    """
    class_name      = models.CharField(max_length=150,
                          help_text="e.g. 'Fitness Class', 'Yoga Training Class'")
    trainer         = models.ForeignKey('Trainer', on_delete=models.SET_NULL,
                          null=True, blank=True, related_name='schedules')

    # Slot 1
    slot_1_day      = models.CharField(max_length=20, choices=DAY_CHOICES)
    slot_1_time     = models.CharField(max_length=50,
                          help_text="e.g. '10:00AM - 11:30AM'")

    # Slot 2
    slot_2_day      = models.CharField(max_length=20, choices=DAY_CHOICES)
    slot_2_time     = models.CharField(max_length=50,
                          help_text="e.g. '2:00PM - 3:30PM'")

    is_active       = models.BooleanField(default=True)

    order_with_respect_to = None

    class Meta(OrderedModel.Meta):
        verbose_name = "Schedule Entry"
        verbose_name_plural = "Schedule Entries"

    def __str__(self):
        return f"{self.class_name} ({self.slot_1_day} / {self.slot_2_day})"


# ─────────────────────────────────────────────
# TRAINERS
# ─────────────────────────────────────────────

class TrainersSection(SingletonModel):
    """
    Controls the heading of the #trainers section.
    HTML equivalent: <section id="trainers"> .section-heading
    """
    section_title       = models.CharField(max_length=100, default="Expert")
    section_title_em    = models.CharField(max_length=100, default="Trainers")
    section_description = models.TextField(
        default="Nunc urna sem, laoreet ut metus id...")

    class Meta:
        verbose_name = "Trainers Section Heading"

    def __str__(self):
        return "Trainers Section Heading"


class Trainer(OrderedModel):
    """
    One trainer card in the #trainers section.
    HTML equivalent: <div class="trainer-item">
    """
    photo           = models.ImageField(upload_to='trainers/',
                          help_text="Portrait photo of the trainer")
    photo_alt       = models.CharField(max_length=200, blank=True)
    specialty       = models.CharField(max_length=150,
                          help_text="Role shown above name, e.g. 'Strength Trainer'")
    name            = models.CharField(max_length=150,
                          help_text="Full name, e.g. 'Bret D. Bowers'")
    bio             = models.TextField(help_text="Short bio paragraph")

    # Social links — blank = hidden in template
    facebook_url    = models.URLField(blank=True)
    twitter_url     = models.URLField(blank=True)
    linkedin_url    = models.URLField(blank=True)
    behance_url     = models.URLField(blank=True)
    is_active       = models.BooleanField(default=True)

    order_with_respect_to = None

    class Meta(OrderedModel.Meta):
        verbose_name = "Trainer"
        verbose_name_plural = "Trainers"

    def __str__(self):
        return f"{self.name} — {self.specialty}"


# ─────────────────────────────────────────────
# CONTACT SECTION
# ─────────────────────────────────────────────

class ContactSection(SingletonModel):
    """
    Controls the Google Maps embed URL in the contact section.
    The contact form fields are functional, not CMS-managed.
    HTML equivalent: <section id="contact-us"> iframe src
    """
    google_maps_embed_url = models.URLField(
        max_length=1000,
        default="https://maps.google.com/maps?q=...",
        help_text="Paste the full iframe src URL from Google Maps > Share > Embed a map")
    map_height      = models.PositiveIntegerField(default=600,
                          help_text="Height of the map iframe in pixels")

    class Meta:
        verbose_name = "Contact Section"

    def __str__(self):
        return "Contact Section"


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────

class SiteFooter(SingletonModel):
    """
    Controls the footer copyright text.
    HTML equivalent: <footer> <p>Copyright...</p>
    """
    copyright_text  = models.CharField(max_length=300,
                          default="Copyright © 2024 Training Studio",
                          help_text="Copyright line. Year is shown as typed.")
    show_designer_credit = models.BooleanField(default=True,
                          help_text="Show 'Designed by TemplateMo' line")

    class Meta:
        verbose_name = "Site Footer"

    def __str__(self):
        return "Site Footer"