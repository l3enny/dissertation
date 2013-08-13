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
badd +39 OUTLINE.md
badd +582 chapterstheorytheory.tex
badd +1 chaptersintroductiondiagnostics.txt
badd +1 mathcommands.tex
badd +1 chaptersexperimentexperiment.tex
badd +7 TODO.md
badd +7 acronyms.tex
badd +311 chapters/experiment/experiment.tex
badd +648 chapters/metastables/metastables.tex
badd +896 chapters/modeling/modeling.tex
badd +14 chapters/theory/theory.tex
badd +1 ~/tmp
badd +45 ~/tmp/test.tex
badd +242 chapters/introduction/introduction.tex
badd +53 chapters/oes/oes.tex
badd +116 ~/Dropbox/school/fellowships/gsrp/Final\ Report/chapters/oes/oes.tex
badd +188 tex/thesis-umich.cls
badd +1 chapters/emissions/emissions.tex
silent! argdel *
edit chapters/emissions/emissions.tex
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
exe 'vert 1resize ' . ((&columns * 90 + 90) / 180)
exe '2resize ' . ((&lines * 31 + 32) / 64)
exe 'vert 2resize ' . ((&columns * 89 + 90) / 180)
exe '3resize ' . ((&lines * 30 + 32) / 64)
exe 'vert 3resize ' . ((&columns * 89 + 90) / 180)
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
let s:l = 110 - ((45 * winheight(0) + 31) / 62)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
110
normal! 0
wincmd w
argglobal
edit chapters/introduction/introduction.tex
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 338 - ((15 * winheight(0) + 15) / 31)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
338
normal! 01l
lcd ~/Repos/dissertation
wincmd w
argglobal
edit ~/Repos/dissertation/OUTLINE.md
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 37 - ((0 * winheight(0) + 15) / 30)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
37
normal! 05l
lcd ~/Repos/dissertation
wincmd w
exe 'vert 1resize ' . ((&columns * 90 + 90) / 180)
exe '2resize ' . ((&lines * 31 + 32) / 64)
exe 'vert 2resize ' . ((&columns * 89 + 90) / 180)
exe '3resize ' . ((&lines * 30 + 32) / 64)
exe 'vert 3resize ' . ((&columns * 89 + 90) / 180)
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
