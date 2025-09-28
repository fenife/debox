
# Incremental completion on zsh: 实时补全
# source $ZSH_CUSTOM/plugins/incr/incr.zsh

# 关闭自动更新
zstyle ':omz:update' mode disabled

# 解决zsh粘贴卡慢问题
pasteinit() {
  OLD_SELF_INSERT=${${(s.:.)widgets[self-insert]}[2,3]}
  zle -N self-insert url-quote-magic # I wonder if you'd need `.url-quote-magic`?
}

pastefinish() {
  zle -N self-insert $OLD_SELF_INSERT
}
zstyle :bracketed-paste-magic paste-init pasteinit
zstyle :bracketed-paste-magic paste-finish pastefinish
