export default {
  nav: {
    home: 'Главная',
    login: 'Вход',
    register: 'Регистрация',
    logout: 'Выход',
    dashboard: 'Панель управления',
    verify: 'Подтверждение', 
  },
  verify: {
    email: 'Почта',
    code: 'Код подтверждения',
    submit: 'Подтвердить',
    loading: 'Проверка…',
    success: 'Успешно подтверждено!',
    redirecting: 'Перенаправление…',
    error: 'Не удалось подтвердить'
  },
  register: {
    firstName: 'Имя',
    lastName: 'Фамилия',
    email: 'Почта',
    password: 'Пароль',
    submit: 'Зарегистрироваться',
    loading: 'Загрузка...',
    success: 'Регистрация прошла успешно! Перенаправление на вход…',
    error: 'Не удалось зарегистрироваться',
    verificationSent: 'Письмо с подтверждением отправлено, проверьте вашу почту.'
  },
  home: {
    welcome: 'Добро пожаловать',
    prompt: 'Чтобы загружать свой транскрипт, пожалуйста,',
    or: 'или'
  },
  login: {
    email: 'Почта',
    password: 'Пароль',
    submit: 'Войти',
    loading: 'Загрузка...',
    error: 'Ошибка входа'
  },
  dashboard: {
    greeting: 'Привет, {firstName} {lastName}!',
    role: 'Роль: {role}'
  },
  upload: {
    upload_transcript_and_curriculum: 'Загрузить транскрипт и учебный план',
    transcript_upload: 'Транскрипт',
    choose_pdf: 'Выберите PDF',
    sending: 'Отправка...',
    send: 'Отправить',
    curriculum_upload: 'Учебный план',
    choose_xlsx: 'Выберите XLSX',
  },
  student: {
    student_info: 'Информация о студенте',
    name: 'ФИО',
    faculty: 'Факультет',
    program_code: 'Код программы',
    program_name: 'Название программы',
    program_group: 'Группа программ',
    entry_year: 'Год поступления',
    language: 'Язык обучения',
    gpa: 'GPA',
    total_credits: 'Кредиты всего',
  },
  courses: {
    courses: 'Курсы',
    course_name: 'Название',
    credits: 'Кредиты',
    traditional: 'Традиционная',
    retake: 'Ретейк',
    headers: {
      index: '№',
      percent: '%',
      traditional: 'Традиционная',
      blockCode: 'Код блока',
      disciplineCode: 'Шифр дисциплины',
      disciplineName: 'Название программы',
      disciplineType: 'Цикл дисциплин',
      prerequisite: 'Предварительное требование',
      contactHours: 'Контактных часов в неделю',
      examType: 'Тип экзамена',
      module: 'Шифр модуля',
      credits: 'Кредиты',
    }
  },
  curriculum: {
    curriculum_metadata: 'Данные программы',
    intake_year: 'Год набора',
    total_credits: 'Всего кредитов',
  },
  tabs: {
    course_short: 'курс',
    fall: 'Осень',
    spring: 'Весна',
  },
  electives: {
    electives: 'Элективы',
    group: 'Группа',
  },
  general: {
    download_json: 'Скачать JSON',
    no_courses: 'Нет курсов',
  }
}
