const generated_strings = {
    {% for lang, translations in strings.items() %}
        {{ lang|lower }}: {
            {% for key, value in translations.items() %}
                {{ key }}: {{ value|tojson }},
            {% endfor %}
        },
    {% endfor %}
}
let ES = Object.assign({}, generated_strings.es, {
    print_alert: "A continuación se abrirá una versión en PDF optimizada para imprimir",
}); // Most strings are hardcoded in the HTML code (TODO: use english as default instead)
const EN = Object.assign({}, generated_strings.en, {
	description: 'I am Jorge Bruned, a Computer Scientist who is passionate about Artificial Intelligence and Software Development',
    about_me: 'About me',
    education: 'Education',
    experience: 'Experience',
    projects: 'Portfolio',
    porfolio: 'Portfolio',
    knowledge: 'Skills',
    contact: 'Contact',
    role_short: 'Computer Scientist & Machine Learning Engineer',
    age: 'Age',
    role: 'Computer Scientist & Engineer',
    years_old: 'years old',
    occupation: 'Occupation',
    email: 'Email',
    email_addr: '******',  // 'contact',
    location_title: 'Location',
    cv: 'CV',
    source: 'Source code',
    blog: 'Blog',
    location_content: 'Pamplona (Spain)<br>Sabiñánigo (Spain)',
    welcome: 'Hi! I am Jorge Bruned, a Computer Scientist & Engineer who is passionate about Artificial Intelligence and Software Development.',
    welcome_2: "Although I specialize in Artificial Intelligence, I'm also passionate about Software Development, and have experience as a front-end developer. " +
               "Among my most remarkable projects so far, the development and deployment of fully-customized web applications for a SME stands out, along with my BSc and MSc theses on Machine Learning research. " +
               "The latter involved the design and training of a computer vision model for a real application in product.",
    sabi: 'Sabiñánigo (Spain)',
    results: 'Results',
    bach_title: 'Science & Techology "Bachillerato"',
    bach_content: 'Last two years of high school in Spain, where you are prepared for University.',
    bach_honors: 'Graduated with honors (Cum Laude)',
    avg_score: 'GPA',  // 'Average score',
    upna: 'Public University of Navarre (Spain)',
    bsc_title: "Bachelor's Degree in Computer Science & Engineering",
    bsc_track: 'Four-year-long degree consisting of 240 ECTS, in which I took the Artificial Intelligence Track',
    bsc_extraord_pre: 'Extraordinary award to the',
    bsc_extraord_bold: 'best academic record',
    bsc_extraord_post: 'in the Computer Engineering BSc',
    bsc_thesis: 'BSc thesis',
	research_on: 'Research on',
	active_learning_desc: "a Machine Learning technique suitable for scenarios where there isn't enough labelled data",
	tfg_nota: "Grade: 10.0, with honors (Cum Laude)",
    cum_laudes: 'courses with honors (Cum Laude)',
    cum_laude: 'with honors (Cum Laude)',
    internationalization: 'Internationalization',
    bsc_internat: 'Large number of courses taken in English (as part of the International Program). International Mobility Program at TU Delft (Erasmus).',
	msc_title: "Master's Degree in Computer Science & Engineering",
    msc_1: "I took this Master's degree while working part-time as a software developer and Machine Learning engineer, which I would say was an excellent way of complementing university's more-theoretical approach with real-life experiences.",
    msc_2: "Moreover, I had the opportunity of carrying out my Master's Thesis at Veridas, in the field of Computer Vision, with a real application in product.",
    msc_thesis: "Master's Thesis",
    instance_segmentation_tfm_main: "Research and application of Instance Segmentation models",
    instance_segmentation_tfm_desc: "a set of object detection techniques that allow to locate and classify objects in an image with great precision",
    tfm_nota: "Grade: 10.0",
    calificacion: "Grade",
    vg_title: 'Video Game and Virtual Reality Application Development (Specialization Diploma)',
    vg_content: 'Six-semester-long program focused on videogame development and AR applications.',
    vg_knowledge: 'Skills',
    vg_knowledge_1: 'Videogame programming (Unity, Unreal...)',
    vg_knowledge_2: 'Physics applied to videogames',
    vg_knowledge_3: '3D modelling & animation (Maya, Blender...)',
    vg_knowledge_4: 'Artificial Intelligence in videogames',
    vg_knowledge_5: 'Pipelines, Scripting & Videogame Production',
    vg_knowledge_6: 'Native application development (Android, iOs)',
    vg_knowledge_7: 'Development of Augmented Reality Applications',
    eras_title: 'Exchange Computer Science',
    eras_content: "Erasmus+ Exchange Program as part of my Bachelor's Degree in Computer Engineering",
    eras_courses: 'Taken courses',
    eras_courses_1: 'Deep Learning',
    eras_courses_2: 'Network Security',
    eras_courses_3: 'Wireless IoT and Local Area Networks',
    eras_courses_4: 'Web Programming Languages',
    certs: 'Languages & Certifications',
    driving_license: '(driving license)',
    clarinet: 'Professional Music Education Diploma (Clarinet)',
    eoi_sabi: "Official Language School (Spain)",
    cpm_sabi: "Professional Music School (Spain)",
    dgt_hue: "Spain",
    experience_brief: "Throughout my career, I have carried out a wide variety of projects, always with the aim of acquiring new knowledge and broadening my horizons",
    project_info: "Project Info",
    m_jan: "January",
    m_feb: "Feburary",
    m_mar: "March",
    m_apr: "April",
    m_may: "May",
    m_jun: "June",
    m_jul: "July",
    m_aug: "August",
    m_sep: "September",
    m_oct: "October",
    m_nov: "November",
    m_dec: "December",
    present: "Present",
    fb_role: "IT manager",
    fb_content: "During several years, I have carried out several sporadic tasks concerning hardware and software deployment, installation and maintenance for this SME." +
        "This experiences have provided me with a broad vision of the real needs of a business and enabled me to face real-life problems.",
    fb_tasks: "Some tasks that I carried out include:",
    fb_tasks_1: "Deployment of a local area network in an industrial unit using Cat6 wiring, set up WiFi networks, DHCP & NAS servers, etc.",
    fb_tasks_2: "Development of a food delivery web application from scratch, focusing on customization and the business's needs.",
    fb_tasks_3: "Installation of a CCTV surveillance system with analog cameras and UTP wiring, besides several IP camaras in different locations.",
    fb_tasks_4: "Deployment and setup of several networks and devices; web, email and SEO management, incident resolution, etc.",
    neuraptic_1: "During a semester as an intern, I had the great opportunity of getting to know how Artificial Intelligence solutions can be applied to real problems (mainly vision). " +
        "Some of my tasks were to replicate previous projects, make some improvements on them, integrate the training and deployment processes in pipelines, etc.",
    neuraptic_2: "I also started my BSc Thesis in the field of Active Learning, which has allowed me to review and implement some state-of-the-art models in the literature.",
	veridas_1: "During my first year, I worked part-time as a frontend developer while taking my Master's degree, focusing on native apps. Some of my tasks included:",
    veridas_1_1: "Libraries and SDKs development, with advanced Kotlin and Gradle knowledge",
    veridas_1_2: "Android apps creation, with MVVM architecture and dependency injection",
    veridas_1_3: "Usage of CI/CD pipelines, shared version control, MRs, agile methodologies and so on",
    veridas2a: "Currently, I'm working part-time as a Machine Learning Engineer focused on computer vision models for identity document analysis, such as object detection, classification, etc.",
    veridas2b: "My tasks range from researching and conceiving new models from scratch to their integration and evaluation in product.",
    portfolio: "Portfolio",
    portfolio_brief: "In this section, some of my projects are listed",
    more_info_web: ".<br>Detailed information about them can be found on my webpage.",
    tag_all: "All",
    tag_soft: "Software Development",
    tag_ai: "Artificial Intelligence",
    tag_hw: "Hardware & Networks",
    hw_soft: "Hardware & Software Dev",
    used_technologies: "Used technologies:",
    access_web: "Enter website",
	knowledge_brief: "Below I have listed a series of skills and aptitudes which I believe to own",
    know_fields: "Fields of Knowledge",
    contact_me: "Contact me!",
    contact_brief: "Don't hesitate to get in touch via email or LinkedIn.",
    pdf_version_warning: "I'd recommend accessing my CV at <a href='https://jorgebruned.com'>jorgebruned.com</a>,<br>where you will always find the last version, and be able to interact with it.",
    pdf_modal_title: "Download as PDF",
    pdf_modal_text: "If you want, you can download an optimized PDF version for printing. However, I recommend you to visit this website, where you will always find the last version, and in an interactive format.",
    // BLOG
    blog_desc_1: "In this section you will find all kinds of content, ranging from status updates to personal projects, topics I have found interesting, etc.",
    blog_desc_2: "I try to publish new content regularly, so stay tuned!",
    curriculum_vitae: "Curriculum Vitae",
    by: "by",
    on: "on",
    in: "in",
    blog_tag_all: "All",
    blog_tag_updates: "Updates",
    blog_tag_projects: "Projects",
    blog_tag_interesting: "Interesting topics",
    more_blog_posts: "More blog posts",
    about_the_author: "About the author",
    print_alert: "An optimized PDF version will be opened"
});
export { ES, EN };