let SessionLoad = 1
if &cp | set nocp | endif
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/Repos/dissertation
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +1 UsersBen.sshgithub_rsa.pub
badd +84 main.tex
badd +581 chaptersintroductionintroduction.tex
badd +16 scratch.txt
badd +1 main.pdf
badd +37 OUTLINE.md
badd +582 chapterstheorytheory.tex
badd +1 chaptersintroductiondiagnostics.txt
badd +1 mathcommands.tex
badd +1 chaptersexperimentexperiment.tex
badd +7 TODO.md
badd +15 acronyms.tex
badd +225 chapters/experiment/experiment.tex
badd +291 chapters/metastables/metastables.tex
badd +259 chapters/modeling/modeling.tex
silent! argdel *
edit chapters/modeling/modeling.tex
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
wincmd _ | wincmd |
split
1wincmd k
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 88 + 88) / 177)
exe '2resize ' . ((&lines * 35 + 36) / 72)
exe 'vert 2resize ' . ((&columns * 88 + 88) / 177)
exe '3resize ' . ((&lines * 34 + 36) / 72)
exe 'vert 3resize ' . ((&columns * 88 + 88) / 177)
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 310 - ((52 * winheight(0) + 35) / 70)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
310
normal! 0
wincmd w
argglobal
edit main.tex
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 74 - ((20 * winheight(0) + 17) / 35)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
74
normal! 039l
wincmd w
argglobal
edit OUTLINE.md
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 37 - ((17 * winheight(0) + 17) / 34)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
37
normal! 0
wincmd w
exe 'vert 1resize ' . ((&columns * 88 + 88) / 177)
exe '2resize ' . ((&lines * 35 + 36) / 72)
exe 'vert 2resize ' . ((&columns * 88 + 88) / 177)
exe '3resize ' . ((&lines * 34 + 36) / 72)
exe 'vert 3resize ' . ((&columns * 88 + 88) / 177)
tabnext 1
if exists('s:wipebuf')
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20 shortmess=filnxtToO
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
