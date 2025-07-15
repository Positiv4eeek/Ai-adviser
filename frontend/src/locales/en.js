export default {
  nav: {
    home: 'Home',
    login: 'Login',
    register: 'Register',
    logout: 'Logout',
    dashboard: 'Dashboard',
    verify:    'Verify',
    upload_curriculum: 'Upload Curriculum',
    list_curriculum: 'Curriculum List',
  },
  verify: {
    email: 'Email',
    code: 'Verification Code',
    submit: 'Verify',
    loading: 'Verifying…',
    success: 'Successfully verified!',
    redirecting: 'Redirecting…',
    error: 'Verification failed'
  },
  register: {
    firstName: 'First Name',
    lastName: 'Last Name',
    email: 'Email',
    password: 'Password',
    submit: 'Register',
    loading: 'Loading...', 
    success: 'Registration successful!',
    error: 'Registration failed',
    verificationSent: 'A verification email has been sent. Please check your inbox.'
  },
  login: {
    email: 'Email',
    password: 'Password',
    submit: 'Login',
    loading: 'Loading...',
    error: 'Login failed'
  },
  home: {
    welcome: 'Welcome',
    prompt: 'To upload your transcript, please',
    or: 'or'
  },
  dashboard: {
    loading: 'Loading...',
    greeting: 'Hello, {firstName} {lastName}!',
    role: 'Role: {role}'
  },
  upload: {
    upload_new_transcript: "Upload New Transcript",
    upload_transcript: 'Upload transcript',
    upload_curriculum: 'Upload curriculum',
    transcript_upload: 'Transcript',
    choose_pdf: 'Choose PDF',
    sending: 'Sending...',
    send: 'Send',
    curriculum_upload: 'Curriculum',
    choose_xlsx: 'Choose XLSX',
    saved_id: "Saved with ID {id}",
  },
  student: {
    student_info: 'Student Info',
    name: 'Name',
    faculty: 'Faculty',
    program_code: 'Program Code',
    program_name: 'Program Name',
    program_group: 'Program Group',
    entry_year: 'Entry Year',
    language: 'Language',
    gpa: 'GPA',
    total_credits: 'Total Credits',
  },
  courses: {
    courses: 'Courses',
    course_name: 'Course Name',
    credits: 'Credits',
    traditional: 'Traditional',
    retake: 'Retake',
    headers: {
      index: '#',
      percent: '%',
      traditional: 'Traditional',
      blockCode: 'Block Code',
      disciplineCode: 'Discipline Code',
      disciplineName: 'Program Name',
      disciplineType: 'Discipline Type',
      prerequisite: 'Prerequisite',
      contactHours: 'Contact hours per week',
      examType: 'Exam Type',
      module: 'Module Code',
      credits: 'Credits',
    }
  },
  curriculum: {
    choose_plan: 'Choose Curriculum',
    select_placeholder: 'Select',
    program_code: 'Program Code',
    program_name: 'Program Name',
    program_group: 'Program Group',
    curriculum_metadata: 'Curriculum Data',
    intake_year: 'Intake Year',
    total_credits: 'Total Credits',
  },
  tabs: {
    course_short: 'course',
    fall: 'Fall',
    spring: 'Spring',
  },
  electives: {
    electives: 'Electives',
    group: 'Group',
  },
  general: {
    loading: 'Loading...',
    download_json: 'Download JSON',
    no_courses: 'No courses',
  }
}