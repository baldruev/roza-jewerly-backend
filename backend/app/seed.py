from django.db import transaction

from backend.app.models.products import Category, Product


# Очистка существующих данных (опционально)
@transaction.atomic
def clear_data():
    Product.objects.all().delete()
    Category.objects.all().delete()

# Данные для заполнения
def run_seed():
    clear_data()
    
    # --- Создание категорий ---
    
    # 1. Rings
    rings = Category.objects.create(slug='rings', order=10)
    rings.set_current_language('en')
    rings.name = 'Rings'
    rings.description = 'Wedding, engagement, and decorative rings.'
    rings.set_current_language('de')
    rings.name = 'Ringe'
    rings.description = 'Eheringe, Verlobungsringe und Zierringe.'
    rings.set_current_language('fr')
    rings.name = 'Bagues'
    rings.description = 'Alliances, bagues de fiançailles et bagues décoratives.'
    rings.save()

    # 2. Earrings
    earrings = Category.objects.create(slug='earrings', order=20)
    earrings.set_current_language('en')
    earrings.name = 'Earrings'
    earrings.description = 'From elegant studs to luxurious chandeliers.'
    earrings.set_current_language('de')
    earrings.name = 'Ohrringe'
    earrings.description = 'Von eleganten Steckern bis hin zu luxuriösen Kronleuchtern.'
    earrings.set_current_language('fr')
    earrings.name = 'Boucles d\'oreilles'
    earrings.description = 'Des clous élégants aux lustres luxueux.'
    earrings.save()

    # 3. Necklaces & Pendants
    necklaces = Category.objects.create(slug='necklaces', order=30)
    necklaces.set_current_language('en')
    necklaces.name = 'Necklaces & Pendants'
    necklaces.description = 'Fine chains, pendants, and statement necklaces.'
    necklaces.set_current_language('de')
    necklaces.name = 'Halsketten & Anhänger'
    necklaces.description = 'Feine Ketten, Anhänger und opulente Colliers.'
    necklaces.set_current_language('fr')
    necklaces.name = 'Colliers & Pendentifs'
    necklaces.description = 'Chaînes fines, pendentifs et colliers imposants.'
    necklaces.save()

    # 4. Bracelets
    bracelets = Category.objects.create(slug='bracelets', order=40)
    bracelets.set_current_language('en')
    bracelets.name = 'Bracelets'
    bracelets.description = 'Bangles, chain bracelets, and charm bracelets.'
    bracelets.set_current_language('de')
    bracelets.name = 'Armbänder'
    bracelets.description = 'Armreifen, Gliederarmbänder und Bettelarmbänder.'
    bracelets.set_current_language('fr')
    bracelets.name = 'Bracelets'
    bracelets.description = 'Bracelets joncs, chaînes et bracelets à breloques.'
    bracelets.save()

    # 5. Brooches
    brooches = Category.objects.create(slug='brooches', order=50)
    brooches.set_current_language('en')
    brooches.name = 'Brooches'
    brooches.description = 'Classic and modern designer brooches.'
    brooches.set_current_language('de')
    brooches.name = 'Broschen'
    brooches.description = 'Klassische und moderne Designer-Broschen.'
    brooches.set_current_language('fr')
    brooches.name = 'Broches'
    brooches.description = 'Broches de créateurs classiques et modernes.'
    brooches.save()

    # --- Создание продуктов ---
    
    product_data = [
        # Rings
        {'sku': 'RG001', 'category': rings, 'price': 1200.00, 'material': 'White Gold', 'weight': 3.5, 'translations': {
            'en': {'name': 'Eternity Ring', 'description': 'An elegant white gold ring with a diamond band.'},
            'de': {'name': 'Ewigkeitsring', 'description': 'Ein eleganter Weißgoldring mit Diamantband.'},
            'fr': {'name': 'Bague Éternité', 'description': 'Une élégante bague en or blanc avec une bande de diamants.'}
        }},
        {'sku': 'RG002', 'category': rings, 'price': 850.50, 'material': 'Yellow Gold, Sapphire', 'weight': 4.2, 'translations': {
            'en': {'name': 'Royal Blue Ring', 'description': 'An engagement ring with a large sapphire surrounded by diamonds.'},
            'de': {'name': 'Königsblauer Ring', 'description': 'Ein Verlobungsring mit einem großen Saphir, umgeben von Diamanten.'},
            'fr': {'name': 'Bague Bleu Royal', 'description': 'Une bague de fiançailles avec un grand saphir entouré de diamants.'}
        }},
        {'sku': 'RG003', 'category': rings, 'price': 450.00, 'material': 'Rose Gold', 'weight': 2.8, 'translations': {
            'en': {'name': 'Minimalist Knot Ring', 'description': 'A delicate rose gold ring in the shape of a knot.'},
            'de': {'name': 'Minimalistischer Knotenring', 'description': 'Ein zarter Roségoldring in Form eines Knotens.'},
            'fr': {'name': 'Bague Nœud Minimaliste', 'description': 'Une bague délicate en or rose en forme de nœud.'}
        }},

        # Earrings
        {'sku': 'ER001', 'category': earrings, 'price': 780.00, 'material': 'Platinum, Diamonds', 'weight': 5.0, 'translations': {
            'en': {'name': 'Sparkle Stud Earrings', 'description': 'Classic round diamond stud earrings.'},
            'de': {'name': 'Funkelnde Ohrstecker', 'description': 'Klassische runde Diamant-Ohrstecker.'},
            'fr': {'name': 'Puces d\'oreilles "Étincelle"', 'description': 'Puces d\'oreilles classiques avec diamants ronds.'}
        }},
        {'sku': 'ER002', 'category': earrings, 'price': 1500.00, 'material': 'Yellow Gold, Emeralds', 'weight': 8.5, 'translations': {
            'en': {'name': 'Eden Chandelier Earrings', 'description': 'Luxurious chandelier earrings with cascading emeralds.'},
            'de': {'name': 'Eden Kronleuchter-Ohrringe', 'description': 'Luxuriöse Kronleuchter-Ohrringe mit kaskadierenden Smaragden.'},
            'fr': {'name': 'Boucles d\'oreilles lustre "Éden"', 'description': 'Luxueuses boucles d\'oreilles lustre avec des émeraudes en cascade.'}
        }},
        {'sku': 'ER003', 'category': earrings, 'price': 320.00, 'material': 'Silver', 'weight': 6.2, 'translations': {
            'en': {'name': 'Geometric Hoop Earrings', 'description': 'Modern silver hoop earrings with a geometric pattern.'},
            'de': {'name': 'Geometrische Kreolen', 'description': 'Moderne silberne Kreolen mit geometrischem Muster.'},
            'fr': {'name': 'Créoles Géométriques', 'description': 'Créoles modernes en argent avec un motif géométrique.'}
        }},
        
        # Necklaces
        {'sku': 'NK001', 'category': necklaces, 'price': 950.00, 'material': 'Rose Gold, Rose Quartz', 'weight': 7.0, 'translations': {
            'en': {'name': 'Tenderness Necklace', 'description': 'Necklace with a large rose quartz pendant.'},
            'de': {'name': 'Halskette "Zärtlichkeit"', 'description': 'Halskette mit einem großen Rosenquarz-Anhänger.'},
            'fr': {'name': 'Collier "Tendresse"', 'description': 'Collier avec un grand pendentif en quartz rose.'}
        }},
        {'sku': 'NK002', 'category': necklaces, 'price': 550.00, 'material': 'Silver, Pearl', 'weight': 12.0, 'translations': {
            'en': {'name': 'Classic Pearl Necklace', 'description': 'A classic necklace made of natural freshwater pearls.'},
            'de': {'name': 'Klassische Perlenkette', 'description': 'Eine klassische Halskette aus natürlichen Süßwasserperlen.'},
            'fr': {'name': 'Collier de Perles Classique', 'description': 'Un collier classique en perles d\'eau douce naturelles.'}
        }},
        {'sku': 'NK003', 'category': necklaces, 'price': 250.00, 'material': 'Yellow Gold', 'weight': 2.5, 'translations': {
            'en': {'name': 'Sunbeam Thin Chain', 'description': 'A delicate yellow gold chain for everyday wear.'},
            'de': {'name': 'Dünne Kette "Sonnenstrahl"', 'description': 'Eine zarte Gelbgoldkette für den Alltag.'},
            'fr': {'name': 'Chaîne fine "Rayon de Soleil"', 'description': 'Une délicate chaîne en or jaune à porter au quotidien.'}
        }},

        # Bracelets
        {'sku': 'BR001', 'category': bracelets, 'price': 680.00, 'material': 'Silver', 'weight': 15.0, 'translations': {
            'en': {'name': 'Manhattan Bangle', 'description': 'A wide, polished silver bangle bracelet.'},
            'de': {'name': 'Manhattan Armreif', 'description': 'Ein breiter, polierter Silber-Armreif.'},
            'fr': {'name': 'Bracelet Manchette "Manhattan"', 'description': 'Un large bracelet manchette en argent poli.'}
        }},
        {'sku': 'BR002', 'category': bracelets, 'price': 420.00, 'material': 'Yellow Gold', 'weight': 9.5, 'translations': {
            'en': {'name': 'Venetian Chain Bracelet', 'description': 'A classic Venetian weave chain bracelet.'},
            'de': {'name': 'Venezianisches Gliederarmband', 'description': 'Ein klassisches Armband mit venezianischem Geflecht.'},
            'fr': {'name': 'Bracelet chaîne Vénitienne', 'description': 'Un bracelet chaîne classique à maille vénitienne.'}
        }},
        {'sku': 'BR003', 'category': bracelets, 'price': 890.00, 'material': 'Silver, Charms', 'weight': 25.0, 'translations': {
            'en': {'name': 'Your Story Charm Bracelet', 'description': 'A bracelet base to build your own charm collection.'},
            'de': {'name': 'Dein-Märchen-Bettelarmband', 'description': 'Eine Armbandbasis, um deine eigene Charm-Sammlung aufzubauen.'},
            'fr': {'name': 'Bracelet à breloques "Ton Histoire"', 'description': 'Une base de bracelet pour créer votre propre collection de breloques.'}
        }},
        
        # Brooches
        {'sku': 'BC001', 'category': brooches, 'price': 1100.00, 'material': 'Platinum, Sapphires', 'weight': 11.2, 'translations': {
            'en': {'name': 'Bird of Paradise Brooch', 'description': 'An exquisite bird-shaped brooch adorned with sapphires.'},
            'de': {'name': 'Paradiesvogel-Brosche', 'description': 'Eine exquisite vogelförmige Brosche, verziert mit Saphiren.'},
            'fr': {'name': 'Broche "Oiseau de Paradis"', 'description': 'Une broche exquise en forme d\'oiseau, ornée de saphirs.'}
        }},
        {'sku': 'BC002', 'category': brooches, 'price': 350.00, 'material': 'Yellow Gold, Enamel', 'weight': 6.8, 'translations': {
            'en': {'name': 'Maple Leaf Brooch', 'description': 'A maple leaf shaped brooch covered in colored enamel.'},
            'de': {'name': 'Ahornblatt-Brosche', 'description': 'Eine ahornblattförmige Brosche, überzogen mit farbigem Email.'},
            'fr': {'name': 'Broche "Feuille d\'érable"', 'description': 'Une broche en forme de feuille d\'érable recouverte d\'émail coloré.'}
        }},
        {'sku': 'BC003', 'category': brooches, 'price': 580.00, 'material': 'Silver, Marcasite', 'weight': 9.0, 'translations': {
            'en': {'name': 'Art Deco Brooch', 'description': 'A geometric Art Deco style brooch with marcasite stones.'},
            'de': {'name': 'Art-déco-Brosche', 'description': 'Eine geometrische Brosche im Art-déco-Stil mit Markasitsteinen.'},
            'fr': {'name': 'Broche Art Déco', 'description': 'Une broche géométrique de style Art déco avec des marcassites.'}
        }}
    ]

    with transaction.atomic():
        for data in product_data:
            translations = data.pop('translations')
            # Устанавливаем язык по умолчанию (английский) для непереводимых полей
            product = Product.objects.create(**data) 
            for lang_code, trans_data in translations.items():
                product.set_current_language(lang_code)
                product.name = trans_data['name']
                product.description = trans_data['description']
            product.save()

# Для запуска раскомментируйте следующие строки:
run_seed()
print("Database has been seeded with English, German, and French data!")