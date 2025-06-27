from modeltranslation.translator import translator, TranslationOptions
from .models import EventCategory, Location, Event, Partner # Import relevant models

# Note: If your original 'name' field in EventCategory is unique=True,
# consider if you truly want a translated 'name' field.
# For choices, modeltranslation has specific ways to handle them if you want choices translated.

class EventCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description',) # Fields to be translated.
    # By default, translated fields inherit null/blank from the original field.
    # If 'name' in models.py is NOT null=True, its translations will also be NOT NULL.
    # If you need name_en to be nullable, your base 'name' field would need null=True or you'd handle it via default.

class LocationTranslationOptions(TranslationOptions):
    fields = ('name', 'address', 'accessibility', 'contact_person',)

class PartnerTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'contact_person',)

class EventTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'target_audience', 'program',) # contact_phone is less likely to be translated

# Register your models for translation
translator.register(EventCategory, EventCategoryTranslationOptions)
translator.register(Location, LocationTranslationOptions)
translator.register(Partner, PartnerTranslationOptions)
translator.register(Event, EventTranslationOptions)