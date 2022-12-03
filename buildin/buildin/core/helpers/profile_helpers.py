def get_phone_number(profile):
    phone_number = profile.phone_number
    phone_number.replace(', press', '/')
    return phone_number
