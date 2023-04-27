SELECT s.section_id, s.section_name, cc.content_name, cc.content_description, cc.content_type, 
       cs.slide_name, cs.slide_description, cs.slide_link, 
       cl.link_name, cl.link_description, cl.link_link, 
       cf.file_name, cf.file_description, cf.file_link 
FROM CourseContent cc
LEFT JOIN Section s ON cc.section_id = s.section_id
LEFT JOIN CourseSlide cs ON cc.course_content_id = cs.course_content_id
LEFT JOIN CourseLink cl ON cc.course_content_id = cl.course_content_id
LEFT JOIN CourseFile cf ON cc.course_content_id = cf.course_content_id
WHERE s.course_code = :course_code
ORDER BY s.section_name, cc.section_id, cc.course_content_id;