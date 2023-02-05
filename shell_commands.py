# Создать двух пользователей (с помощью метода User.objects.create_user('username')).
u1 = User.objects.create_user('Galym')
u2 = User.objects.create_user('Marat')

# Создать два объекта модели Author, связанные с пользователями.
au1 = Author.objects.create(user_id=1)
au2 = Author.objects.create(user_id=2)

# Добавить 4 категории в модель Category.
cat1 = Category.objects.create(name='Development')
cat2 = Category.objects.create(name='Design')
cat3 = Category.objects.create(name='Management')
cat4 = Category.objects.create(name='Marketing')

# Добавить 2 статьи и 1 новость.
p1 = Post.objects.create(author=au1, type='p', title='Концепции Rust, которые неплохо бы знать пораньше', post_body=
'''Весь минувший месяц я глаз не мог оторвать от языка программирования Rust, ведь его конёк – создание современных программ, обеспечивающих безопасную работу с памятью. За прошедшие годы появилось несколько языков, которые позиционировались как «инструмент что надо» для написания надёжного бекенд-софта. Постепенно маятник качнулся от Java/C++ к Go и Rust, выстроенных на многолетних разработках по теории языков программирования. Суть – в создании инструментов, которые были бы эффективны именно в наш век.''')

p2 = Post.objects.create(author=au2, type='p', title='Всё про USB-C: введение для электронщиков', post_body=
'''Прошло уже почти пять лет, как во всевозможных устройствах начали появляться порты USB-C. Это стандарт, за рамки которого могут выходить многие производители и электронщики. Поначалу существовало много путаницы относительно того, что он в себе несёт, и всяческие отклонения со стороны производителей некоторых людей отталкивали. Однако теперь USB-C уже прочно вошёл в нашу жизнь, и я хочу показать вам, как именно этот стандарт используется, чего могут ожидать от него пользователи, а что он способен предложить электронщикам.''')

n1 = Post.objects.create(author=au1, type='n', title='Десктопная версия Google Chrome получит редизайн вкладок и закладок', post_body=
'''Google планирует «освежить» внешний вид Chrome. Работа над редизайном идёт как минимум с ноября. Сейчас эти изменения видны в Chrome Canary. По умолчанию параметр отключён, но его можно включить с помощью флага chrome://flags/#chrome-refresh-2023. Эта опция также есть в последних сборках Chromium. 

В Windows редизайн Google Chrome обеспечивает более чёткое разделение вкладок и омнибара, а фоновые вкладки приобретают характерный синий оттенок. Закладки приобрели закруглённые формы для текстовых полей и кнопок. ''')

# Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
p1.category.add(cat1)
p1.category.add(cat4)
p2.category.add(cat2)
p2.category.add(cat3)
p2.category.add(cat4)
n1.category.add(cat3)

# Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
com1_p1_u1 = Comment.objects.create(post=p1, commenter=u1, comment_body=
'''Не совсем понимаю RUST, с чего начать?''')

com2_p2_u1 = Comment.objects.create(post=p2, commenter=u1, comment_body=
'''На горизонте маячит появление стандарта USB 4, который будет аналогичен ThunderBolt, но не во всём — только пока не ясно в лучшую или худшую сторону.''')

com3_p2_u2 = Comment.objects.create(post=p2, commenter=u2, comment_body=
'''А есть ли удобное описание протокол PD?''')

com4_n1_u2 = Comment.objects.create(post=n1, commenter=u2, comment_body=
'''Закругленные закладки - это то, чего все ждали. Кажется, закладки - это боль не только Хрома, а вообще любой системы, где они есть.''')

# Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
# Допускаем отрицательный рейтинг, например для com3_p2_u2
p1.like()
p1.like()
p1.like()
p1.like()
p1.like()

p2.like()
p2.like()
p2.dislike()
p2.like()
p2.like()
p2.like()
p2.dislike()

n1.like()
n1.dislike()
n1.like()

com1_p1_u1.like()
com1_p1_u1.dislike()
com1_p1_u1.dislike()
com1_p1_u1.like()
com1_p1_u1.like()
com1_p1_u1.like()

com2_p2_u1.like()

com3_p2_u2.dislike()

# Обновить рейтинги пользователей.
au1.update_rating()
au2.update_rating()

# Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
Author.objects.all().order_by('-author_rating').values('user__username','author_rating').first()

# Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
best_post = Post.objects.all().order_by('-post_rating').values('post_created', 'author__user__username', 'post_rating', 'title', Post.values().first()


best_post['preview'] = posts_sorted.preview()).first()
# Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
