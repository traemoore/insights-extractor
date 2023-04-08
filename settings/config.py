std_out_logging = True
supported_file_types = ['.pdf']
invalid_content_regexs = [r'X{2,}']
stop_words = ['na', 'dependent', 'address', 'plans',
              'network', 'nonnetwork', 'additional', 'covered']
keywords = {
    'dental': 5,
    'vision': 5,
    'life': 5,
    'disability': 5,
}

keyword_synonyms = { 
    "dental": [ "orthodontic" , "Endo", "Perio", "Oral"] ,
    "vision": [ "eye", "vision", "lens", "lenses", "contact", "contacts" ] ,
    "life": ["accident", "critical", "illness", "accidental", "dismember", "AD&D"] ,
    "disability": [] ,
}

word_min_length = 3