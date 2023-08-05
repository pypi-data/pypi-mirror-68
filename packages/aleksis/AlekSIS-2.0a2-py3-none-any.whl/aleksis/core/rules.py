from rules import add_perm, always_allow

from .models import Announcement, Group, Person
from .util.predicates import (
    has_any_object,
    has_global_perm,
    has_object_perm,
    has_person,
    is_current_person,
    is_group_owner,
    is_notification_recipient,
)

add_perm("core", always_allow)

# View dashboard
add_perm("core.view_dashboard", has_person)

# Use search
search_predicate = has_person & has_global_perm("core.search")
add_perm("core.search", search_predicate)

# View persons
view_persons_predicate = has_person & (
    has_global_perm("core.view_person") | has_any_object("core.view_person", Person)
)
add_perm("core.view_persons", view_persons_predicate)

# View person
view_person_predicate = has_person & (
    has_global_perm("core.view_person") | has_object_perm("core.view_person") | is_current_person
)
add_perm("core.view_person", view_person_predicate)

# View person address
view_address_predicate = has_person & (
    has_global_perm("core.view_address") | has_object_perm("core.view_address") | is_current_person
)
add_perm("core.view_address", view_address_predicate)

# View person contact details
view_contact_details_predicate = has_person & (
    has_global_perm("core.view_contact_details")
    | has_object_perm("core.view_contact_details")
    | is_current_person
)
add_perm("core.view_contact_details", view_contact_details_predicate)

# View person photo
view_photo_predicate = has_person & (
    has_global_perm("core.view_photo") | has_object_perm("core.view_photo") | is_current_person
)
add_perm("core.view_photo", view_photo_predicate)

# View persons groups
view_groups_predicate = has_person & (
    has_global_perm("core.view_person_groups")
    | has_object_perm("core.view_person_groups")
    | is_current_person
)
add_perm("core.view_person_groups", view_groups_predicate)

# Edit person
edit_person_predicate = has_person & (
    has_global_perm("core.change_person") | has_object_perm("core.change_person")
)
add_perm("core.edit_person", edit_person_predicate)

# Link persons with accounts
link_persons_accounts_predicate = has_person & has_global_perm("core.link_persons_accounts")
add_perm("core.link_persons_accounts", link_persons_accounts_predicate)

# View groups
view_groups_predicate = has_person & (
    has_global_perm("core.view_group") | has_any_object("core.view_group", Group)
)
add_perm("core.view_groups", view_groups_predicate)

# View group
view_group_predicate = has_person & (
    has_global_perm("core.view_group") | has_object_perm("core.view_group")
)
add_perm("core.view_group", view_group_predicate)

# Edit group
edit_group_predicate = has_person & (
    has_global_perm("core.change_group") | has_object_perm("core.change_group")
)
add_perm("core.edit_group", edit_group_predicate)

# Assign child groups to groups
assign_child_groups_to_groups_predicate = has_person & has_global_perm(
    "core.assign_child_groups_to_groups"
)
add_perm("core.assign_child_groups_to_groups", assign_child_groups_to_groups_predicate)

# Edit school information
edit_school_information_predicate = has_person & has_global_perm("core.change_school")
add_perm("core.edit_school_information", edit_school_information_predicate)

# Edit school term
edit_schoolterm_predicate = has_person & has_global_perm("core.change_schoolterm")
add_perm("core.edit_schoolterm", edit_schoolterm_predicate)

# Manage school
manage_school_predicate = edit_school_information_predicate | edit_schoolterm_predicate
add_perm("core.manage_school", manage_school_predicate)

# Manage data
manage_data_predicate = has_person & has_global_perm("core.manage_data")
add_perm("core.manage_data", manage_data_predicate)

# Mark notification as read
mark_notification_as_read_predicate = has_person & is_notification_recipient
add_perm("core.mark_notification_as_read", mark_notification_as_read_predicate)

# View announcements
view_announcements_predicate = has_person & (
    has_global_perm("core.view_announcement")
    | has_any_object("core.view_announcement", Announcement)
)
add_perm("core.view_announcements", view_announcements_predicate)

# Create or edit announcement
create_or_edit_announcement_predicate = has_person & (
    has_global_perm("core.add_announcement")
    & (has_global_perm("core.change_announcement") | has_object_perm("core.change_announcement"))
)
add_perm("core.create_or_edit_announcement", create_or_edit_announcement_predicate)

# Delete announcement
delete_announcement_predicate = has_person & (
    has_global_perm("core.delete_announcement") | has_object_perm("core.delete_announcement")
)
add_perm("core.delete_announcement", delete_announcement_predicate)

# Use impersonate
impersonate_predicate = has_person & has_global_perm("core.impersonate")
add_perm("core.impersonate", impersonate_predicate)

# View system status
view_system_status_predicate = has_person & has_global_perm("core.view_system_status")
add_perm("core.view_system_status", view_system_status_predicate)

# View people menu (persons + objects)
add_perm(
    "core.view_people_menu",
    has_person
    & (
        view_persons_predicate
        | view_groups_predicate
        | link_persons_accounts_predicate
        | assign_child_groups_to_groups_predicate
    ),
)

# View admin menu
view_admin_menu_predicate = has_person & (
    manage_data_predicate
    | manage_school_predicate
    | impersonate_predicate
    | view_system_status_predicate
    | view_announcements_predicate
)
add_perm("core.view_admin_menu", view_admin_menu_predicate)

# View person personal details
view_personal_details_predicate = has_person & (
    has_global_perm("core.view_personal_details")
    | has_object_perm("core.view_personal_details")
    | is_current_person
)
add_perm("core.view_personal_details", view_personal_details_predicate)

# Change site preferences
change_site_preferences = has_person & (
    has_global_perm("core.change_site_preferences")
    | has_object_perm("core.change_site_preferences")
)
add_perm("core.change_site_preferences", change_site_preferences)

# Change person preferences
change_person_preferences = has_person & (
    has_global_perm("core.change_person_preferences")
    | has_object_perm("core.change_person_preferences")
    | is_current_person
)
add_perm("core.change_person_preferences", change_person_preferences)

# Change group preferences
change_group_preferences = has_person & (
    has_global_perm("core.change_group_preferences")
    | has_object_perm("core.change_group_preferences")
    | is_group_owner
)
add_perm("core.change_group_preferences", change_group_preferences)
