from CONFIG.subnav import GLOBAL_SUBNAV

def get_visible_subnav_for_user(user) -> dict:
    ''' Get the visible subnav items for the user.
    
    This function will filter out the subnav items that are not visible to the user.
    '''

    accessible_sections = []
    
    for section in GLOBAL_SUBNAV:
        if section.get('is_active', True):
            accessible_items = []
            
            for item in section['items']:
                if item.get('is_active', True):
                    superuser_required = item.get('superuser_required', False)
                    if superuser_required and not user.is_superuser:
                        continue

                    staff_required = item.get('staff_required', False)
                    if staff_required and not user.is_staff:
                        continue
                    
                    required_subs = item.get('required_subscription')
                    if required_subs is None or (
                        isinstance(required_subs, str) and required_subs == user.subscription.subscription_key) or (
                        isinstance(required_subs, list) and user.subscription.subscription_key in required_subs):
                        accessible_items.append(item)
            
            if accessible_items:
                new_section = section.copy()
                new_section['items'] = accessible_items
                accessible_sections.append(new_section)
    
    return accessible_sections