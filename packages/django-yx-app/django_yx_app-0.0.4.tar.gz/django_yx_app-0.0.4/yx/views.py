from __future__ import absolute_import

# from .management.commands.pull import pull_change
# from .models import Resource

# logger = logging.getLogger(__name__)


# @login_required()
# def xsync(request, username):
# 	acc = get_object_or_404(YxAccount, username=username)
# 	pull_change(acc, refresh_sync=False)
#
# 	nxt = request.GET.get('next') or 'index'
# 	return redirect(nxt)


# @login_required
# def get_notes(request, username):
# 	user = get_object_or_404(YxAccount, username=username)

# 	# daterange = request.GET.get('daterange')
# 	# filters = {}
# 	# if daterange == 'today':
# 	#     filters['updated__gte'] = 0
# 	#     filters['updated__lte'] = 1

# 	notes = user.notes.all().order_by('created')
# 	return render(request, 'notes/index.html', {
# 		# 'title': daterange,
# 		'notes': notes,
# 	})


# @login_required
# def list_all_objectives(request, username):
# 	account = get_object_or_404(get_user_model(), username=username)
# 	obj_tag = get_object_or_404(account.tags, name='objective')
# 	objs = obj_tag.notes.all()

# 	orderfield = request.GET.get('orderfield', 'created')
# 	objs = objs.order_by(orderfield)

# 	return render(request, 'okr/index.html', {'title': 'Objectives', 'objectives': objs})


# @login_required
# def get_tasklist(request, username):
# 	acc = get_object_or_404(get_user_model(), username=username)
# 	tasktag = get_object_or_404(acc.tags, name='task')
# 	tasks = tasktag.notes.all().order_by('reminder_time', 'created')
# 	return render(request, 'tasks/tasks-list.html', {'title': 'All tasks', 'tasks': tasks})


# @login_required()
# def list_all_tags(request, username):
# 	user = get_object_or_404(get_user_model(), username=username)
# 	query = user.tags.all().annotate(
# 		note_count=Count('notes'), last_updated=Max('notes__created')).order_by('-last_updated')

# 	if not settings.DEBUG:
# 		logger.debug('exclude note_count=0 in non-debug')
# 		query = query.exclude(note_count=0)

# 	return render(request, 'tags/index.html', {
# 		'tags': query,
# 	})


# @login_required
# def get_shopping_list(request, username):
# 	acc = get_object_or_404(YxAccount, username=username)
# 	shopping_tag = get_object_or_404(acc.tags, name='shopping')
# 	items = shopping_tag.notes.all()
# 	return render(request, 'shopping/index.html', {'title': 'Shopping List', 'items': items})


# @login_required
# def list_all_books(request, username):
# 	acc = get_object_or_404(get_user_model(), username=username)
# 	booktag = get_object_or_404(acc.tags, name='book')
# 	books = booktag.notes.all()
# 	return render(request, 'books/index.html', {'title': 'Books', 'books': books})


# @login_required()
# def view_tagged_notes(request, username, tagnames):
# 	user = get_object_or_404(get_user_model(), username=username)
# 	notes = []
# 	tags = set()
# 	try:
# 		nameset = set(tagnames.split('/'))
# 		tags = set((tag for tag in user.tags.filter(name__in=nameset)))
# 		if tags:
# 			notes = user.notes.filter(tags__in=tags)
# 	except ObjectDoesNotExist:
# 		pass
# 	return render(request, 'notes/index.html', {'notes': notes})


# @login_required
# def synctags(request, username):
# 	acc = get_object_or_404(get_user_model(), username=username)
# 	synctag(acc)
# 	url = reverse('list-all-tags', args=(username,))
# 	return redirect(url)


# @login_required
# def search(request, username):
# 	notes = []
# 	if request.method == 'POST':
# 		form = EnSelectForm(request.POST)
# 		if form.is_valid():
# 			account = get_object_or_404(YxAccount, username=username)
# 			client = account.get_client()
# 			note_store = client.get_note_store()

# 			note_filter = NoteFilter()
# 			note_filter.words = form.cleaned_data['words']  # 'tag:task'
# 			note_filter.order = NoteSortOrder.CREATED
# 			note_filter.ascending = True

# 			spec = NotesMetadataResultSpec()
# 			spec.includeTitle = True
# 			spec.includeCreated = True
# 			spec.includeUpdateSequenceNum = True
# 			spec.includeTagGuids = True
# 			spec.includeAttributes = True

# 			search_result = note_store.findNotesMetadata(account.decrypted_token, note_filter, 0, 5000, spec)
# 			notes = cache_search_result(account, search_result)
# 	else:
# 		form = EnSelectForm()

# 	return render(request, 'yx/search.html', {
# 		'form': form,
# 		'notes': notes,
# 	})


# @login_required
# def viewmeta(request, username, guid):
# 	account = get_object_or_404(YxAccount, username=username)
# 	client = account.get_client()
# 	note_store = client.get_note_store()
# 	yxnote = note_store.getNote(account.decrypted_token, guid,
# 								True,  # content
# 								True,  # res data
# 								False,  # reco
# 								False)  # alter
# 	root = etree.fromstring(yxnote.content)
# 	hash_to_refcount = {}
# 	for media_elm in root.iter('en-media'):
# 		hash = media_elm.attrib['hash']
# 		try:
# 			hash_to_refcount[hash] += 1
# 		except KeyError:
# 			hash_to_refcount[hash] = 1
# 	if yxnote.resources:
# 		for res in yxnote.resources:
# 			res.hash = binascii.hexlify(res.data.bodyHash)
# 			res.refcount = hash_to_refcount.get(res.hash, 0)
# 	return render(request, 'notes/meta.html', {
# 		'note': yxnote,
# 		'resources': yxnote.resources,
# 		'attribute': yxnote.attributes,
# 	})


# @login_required
# def thumbnail(request, username, guid):
# 	filepath = os.path.join(settings.THUMBNAIL_DIR, guid + '.png')
# 	if not os.path.isfile(filepath):
# 		account = get_object_or_404(YxAccount, username=username)
# 		note = get_object_or_404(account.notes, guid=guid)  # check note exists

# 		# post to get
# 		rsp = requests.post(note.thumbnail_url, {'auth': account.decrypted_token})
# 		if rsp.status_code == 200:
# 			try:
# 				os.makedirs(settings.THUMBNAIL_DIR)
# 			except OSError:
# 				pass
# 			open(filepath, 'wb').write(rsp.content)
# 		else:
# 			raise Http404

# 	if os.path.isfile(filepath):
# 		data = open(filepath, 'rb').read()
# 	else:
# 		placeholder_path = os.path.join(os.path.dirname(__file__), 'placeholder.png')
# 		data = open(placeholder_path, 'rb').read()
# 	return HttpResponse(data, content_type='image/png')


# @login_required
# def resource(request, username, reshash):
# 	user = get_object_or_404(YxAccount, username=username)
# 	res = get_object_or_404(Resource, note__yxaccount=user)
# 	mime = res.mime
# 	try:
# 		fp = os.path.join(settings.BASE_DIR, 'files', reshash)
# 		data = open(fp, 'rb').read()
# 	except IOError:  # file not exist
# 		# todo: download it
# 		fp = os.path.join(os.path.dirname(__file__), 'placeholder.png')
# 		data = open(fp, 'rb').read()
# 		mime = 'image/png'
# 	return HttpResponse(data, content_type=mime)
