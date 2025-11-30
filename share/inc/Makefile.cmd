include $(INC_DIR)/Makefile.const
include $(INC_DIR)/Makefile.func

.PHONY: build start stop run pull at attach enter exec sys rund startd

############################################################
# help
############################################################

common: 	## --------------------------------------------- 

help: 	## print help for targets with comments
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s \033[0m%s\n", $$1, $$2}'

cmd:	## print commands
	@LC_ALL=C $(MAKE) -pRrq -f $(firstword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/(^|\n)# Files(\n|$$)/,/(^|\n)# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | grep -E -v -e '^[^[:alnum:]]' -e '^$@$$'

sys: ## print system info
	@echo "-------------------- time info --------------------"
	@echo "now:     $(NOW)"
	@echo "ts:      $(NOW_TS)"
	@echo
	@echo "-------------------- path info --------------------"
	@echo "exec makefile:        $(EXEC_MAKEFILE)"
	@echo "exec makefile path:   $(EXEC_MAKEFILE_PATH)"
	@echo "exec dir:             $(EXEC_DIR)"
	@echo
	@echo "-------------------- system info --------------------"
	-cat /etc/os-release
	@echo
	-cat /etc/lsb-release
	@echo
	cat /proc/version
	@echo
	uname -r
	@echo
	@echo "eth name:  $(ETH_NAME)"
	@echo "host ip:   $(HOST_IP)"
	@echo "host name: $(HOST_NAME)"
	@echo


############################################################
# alias 
############################################################
run: start		## run/start
rund: startd	## run/start daemon
at: enter		## attach to container
attach: enter	## attach to container
exec: enter		## attach to container
st: status		## status

