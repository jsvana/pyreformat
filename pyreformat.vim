function! ToggleArgs()
  let l:winview = winsaveview()
  silent execute "%!pyreformat " . line(".")
  call winrestview(l:winview)
endfunction
nnoremap <Leader>q :call ToggleArgs()<CR>
