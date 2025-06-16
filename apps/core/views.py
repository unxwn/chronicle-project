import json

from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import Board, BoardMember, Note, ChecklistItem
from .forms import BoardForm, NoteForm, QuickNoteForm
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def home(request):
    quick_board, created = Board.objects.get_or_create(
        name='Quick Notes',
        owner=request.user,
        defaults={'color': '#333333'}
    )
    if created:
        BoardMember.objects.create(board=quick_board, user=request.user, role='owner')

    if request.method == 'POST' and 'quick_note_submit' in request.POST:
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.board = quick_board
            note.save()
            messages.success(request, 'Quick note created successfully!')
            return redirect('core:home')
    else:
        form = NoteForm()

    recent_notes = Note.objects.filter(author=request.user).order_by('-updated_at')[:5]
    recent_boards = Board.objects.filter(members=request.user).order_by('-updated_at')[:5]

    return render(request, 'core/pages/home.html', {
        'form': form,
        'recent_notes': recent_notes,
        'recent_boards': recent_boards,
    })


def about_project(request):
    return render(request, 'about_project.html')


def about_core(request):
    return render(request, 'core/pages/about_core.html')


@login_required
def profile(request):
    return render(request, 'core/pages/profile.html', {'user': request.user})


@login_required
def boards_list(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.save()
            BoardMember.objects.create(board=board, user=request.user, role='owner')
            messages.success(request, f'Board "{board.name}" created successfully!')
            return redirect('core:boards_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BoardForm()

    boards = Board.objects.filter(members=request.user).order_by('-updated_at')
    return render(request, 'core/pages/boards_list.html', {
        'form': form,
        'boards': boards,
    })


@login_required
def board_create(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.save()
            BoardMember.objects.create(board=board, user=request.user, role='admin')
            messages.success(request, f'Board "{board.name}" created successfully!')
            return redirect('core:board_detail', board.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BoardForm()
    return render(request, 'core/pages/board_form.html', {'form': form})


@login_required
def board_detail(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    membership = BoardMember.objects.filter(board=board, user=request.user).first()

    if not membership:
        messages.error(request, 'You do not have access to this board.')
        return redirect('core:boards_list')

    can_edit = (request.user == board.owner) or (membership.role in ['owner', 'admin'])

    if request.method == 'POST' and 'board_edit_submit' in request.POST:
        if not can_edit:
            return HttpResponseForbidden()
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            messages.success(request, 'Board updated successfully!')
            return redirect('core:board_detail', board.id)
    else:
        form = BoardForm(instance=board) if can_edit else None

    if request.method == 'POST' and 'note_create_submit' in request.POST:
        note_form = NoteForm(request.POST)
        if note_form.is_valid():
            note = note_form.save(commit=False)
            note.author = request.user
            note.board = board
            note.save()
            messages.success(request, 'Note created successfully!')
            return redirect('core:board_detail', board.id)
    else:
        note_form = NoteForm()

    notes = board.notes.order_by('-updated_at')

    return render(request, 'core/pages/board_detail.html', {
        'board': board,
        'membership': membership,
        'can_edit': can_edit,
        'form': form,
        'note_form': note_form,
        'notes': notes,
    })


@login_required
def board_update(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    bm = board.board_memberships.filter(user=request.user, role__in=['admin', 'editor']).first()

    if board.owner != request.user and not bm:
        messages.error(request, 'You do not have permission to edit this board.')
        return redirect('core:boards_list')

    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            messages.success(request, 'Board updated successfully!')
            return redirect('core:board_detail', board.id)
    else:
        form = BoardForm(instance=board)

    return render(request, 'core/pages/board_form.html', {'form': form, 'board': board})


@login_required
def board_delete(request, board_id):
    board = get_object_or_404(Board, id=board_id)

    if board.owner != request.user:
        messages.error(request, 'Only the board owner can delete this board.')
        return redirect('core:boards_list')

    if request.method == 'POST':
        board_name = board.name
        board.delete()
        messages.success(request, f'Board "{board_name}" deleted successfully!')
        return redirect('core:boards_list')

    return render(request, 'core/pages/board_confirm_delete.html', {'board': board})


@login_required
def notes_list(request):
    notes = Note.objects.filter(author=request.user)
    return render(request, 'core/pages/notes_list.html', {'notes': notes})


@login_required
def note_create(request, board_id):
    board = get_object_or_404(Board, id=board_id)

    if not board.members.filter(id=request.user.id).exists():
        messages.error(request, 'You do not have access to this board.')
        return redirect('core:boards_list')

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.board = board
            note.save()
            messages.success(request, 'Note created successfully!')
            return redirect('core:note_detail', board.id, note.id)
    else:
        form = NoteForm()

    return render(request, 'core/pages/note_form.html', {'form': form, 'board': board})


@login_required
def note_detail(request, board_id, note_id):
    board = get_object_or_404(Board, id=board_id)
    note = get_object_or_404(Note, id=note_id, board=board)

    if not board.members.filter(id=request.user.id).exists():
        messages.error(request, 'You do not have access to this board.')
        return redirect('core:boards_list')

    return render(request, 'core/pages/note_detail.html', {'note': note, 'board': board})


@login_required
def note_update(request, board_id, note_id):
    board = get_object_or_404(Board, id=board_id)
    note = get_object_or_404(Note, id=note_id, board=board)

    if not board.members.filter(id=request.user.id).exists():
        messages.error(request, 'You do not have access to this board.')
        return redirect('core:boards_list')

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated successfully!')
            return redirect('core:note_detail', board.id, note.id)
    else:
        form = NoteForm(instance=note)

    return render(request, 'core/pages/note_form.html', {'form': form, 'board': board, 'note': note})


@login_required
def note_delete(request, board_id, note_id):
    board = get_object_or_404(Board, id=board_id)
    note = get_object_or_404(Note, id=note_id, board=board)

    if not board.members.filter(id=request.user.id).exists():
        messages.error(request, 'You do not have access to this board.')
        return redirect('core:boards_list')

    if request.method == 'POST':
        note_title = note.title
        note.delete()
        messages.success(request, f'Note "{note_title}" deleted successfully!')
        return redirect('core:board_detail', board.id)

    return render(request, 'core/pages/note_confirm_delete.html', {'note': note, 'board': board})


@login_required
@require_POST
def toggle_checklist_item(request, item_id):
    try:
        item = ChecklistItem.objects.get(id=item_id)
    except ChecklistItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)

    board = item.note.board
    if not board.members.filter(id=request.user.id).exists():
        return JsonResponse({'error': 'Access denied'}, status=403)

    try:
        data = json.loads(request.body)
        is_completed = data.get('is_completed', False)
        item.is_completed = is_completed
        item.save()
        return JsonResponse({'is_completed': item.is_completed})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

