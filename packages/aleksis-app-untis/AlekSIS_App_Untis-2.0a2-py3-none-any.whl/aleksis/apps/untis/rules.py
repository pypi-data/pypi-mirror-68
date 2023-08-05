from rules import add_perm

from aleksis.core.util.predicates import has_global_perm, has_person

# Do XML import
do_xml_import_predicate = has_person & has_global_perm("untis.do_xml_import")
add_perm("untis.do_xml_import", do_xml_import_predicate)


# Do XML import
assign_subjects_to_groups_predicate = has_person & has_global_perm(
    "untis.assign_subjects_to_groups"
)
add_perm("untis.assign_subjects_to_groups", assign_subjects_to_groups_predicate)
