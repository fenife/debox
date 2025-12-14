include $(INC_DIR)/Makefile.inc

SIYUAN_IMAGE_TAR=siyuan-$(VERSION).tar.gz

SRC_DIR=./source
SPLIT_DIR=./splits

SRC_TAR=$(SPLIT_DIR)/src_file.tar.gz

pre:	## pre
	mkdir -p $(SRC_DIR)
	mkdir -p $(SPLIT_DIR)

ls:		## ls
	ls -alh $(SRC_DIR)
	@echo
	ls -alh $(SPLIT_DIR)

tar:	## tar
	tar -czvf $(SRC_TAR) $(SRC_DIR)

# -b 3G 表示设置每个分割包的大小，单位还是可以m,k
# -d 参数指定生成的分割包后缀为数字的形式
# -a x来设定序列的长度(默认值是2)，这里设定序列的长度为1
split:		## split
	split -b 9m -d -a 1 $(SRC_TAR) $(SRC_TAR).

zip:
	zip -r file_splits.zip $(SPLIT_DIR)

merge:		## merge
	cat $(SRC_TAR).* > $(SRC_TAR)
	tar -xzvf $(SRC_TAR)

clean:		## clean
	rm -rf $(SPLIT_DIR)/*

rm-tar:		## rm tar
	rm -rf $(SRC_TAR)
	
rm-src:		## rm source
	rm -rf $(SRC_DIR)/*
