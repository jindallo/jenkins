set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'
Plugin 'vim-python/python-syntax'
Plugin 'scrooloose/nerdtree'
Plugin 'kien/ctrlp.vim'
Plugin 'vim-airline/vim-airline'
Plugin 'Yggdroot/indentLine'
Plugin 'tmhedberg/SimpylFold'

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required
" To ignore plugin indent changes, instead use:
"filetype plugin on
"
" Brief help
" :PluginList       - lists configured plugins
" :PluginInstall    - installs plugins; append `!` to update or just :PluginUpdate
" :PluginSearch foo - searches for foo; append `!` to refresh local cache
" :PluginClean      - confirms removal of unused plugins; append `!` to auto-approve removal
"
" see :h vundle for more details or wiki for FAQ
" Put your non-Plugin stuff after this line

syntax on
set number
set expandtab
set tabstop=8
set shiftwidth=4
set softtabstop=4
set autoindent
set hlsearch
set nowrapscan
set t_Co=256
set cursorline
set splitbelow
set splitright
set foldlevelstart=99
set fileformat=unix
set encoding=utf-8
let g:python_highlight_all = 1
highlight CursorLine term=bold cterm=bold
highlight LineNr ctermfg=darkgray
nnoremap <F2>  *N
nnoremap <F3>  N
nnoremap <F4>  n
nnoremap <F5>  :NERDTreeToggle<CR>
nnoremap <F7>  :sv<CR>
nnoremap <F8>  :vs<CR>
nnoremap <space>   za
nnoremap <C-Left>  <C-W>h
nnoremap <C-Down>  <C-W>j
nnoremap <C-Up>    <C-W>k
nnoremap <C-Right> <C-W>l
