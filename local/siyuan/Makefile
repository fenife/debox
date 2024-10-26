
include ../include/Makefile.common


SIYUAN_IMAGE=b3log/siyuan:v3.0.17

pull:
	docker pull m.daocloud.io/docker.io/$(SIYUAN_IMAGE)

tag:
	docker tag m.daocloud.io/docker.io/$(SIYUAN_IMAGE) $(SIYUAN_IMAGE)

SIYUAN_IMAGE_SAVE=./siyuan-v3.0.17.tar
save: 
	if [ -f ${SIYUAN_IMAGE_SAVE} ]; then rm ${SIYUAN_IMAGE_SAVE}; fi
	docker save -o ${SIYUAN_IMAGE_SAVE} ${SIYUAN_IMAGE}

SIYUAN_IMAGE_TAR=siyuan-v3.0.17.tar.gz
tar:
	tar -czvf $(SIYUAN_IMAGE_TAR) $(SIYUAN_IMAGE_SAVE)

define ls_images
	@echo
	ls ./*.tar*
	@echo
	ls ./splits
	@echo
	ls ./merges
	@echo
	docker image ls | grep siyuan
endef

# -b 3G 表示设置每个分割包的大小，单位还是可以m,k
# -d "参数指定生成的分割包后缀为数字的形式
# -a x来设定序列的长度(默认值是2)，这里设定序列的长度为1
split:
	mkdir -p ./splits
	split -b 9m -d -a 1 $(SIYUAN_IMAGE_TAR) ./splits/$(SIYUAN_IMAGE_TAR).
	$(call ls_images)

merge:
	rm -rf ./merges
	mkdir -p ./merges
	cat ./splits/$(SIYUAN_IMAGE_TAR).* > ./merges/$(SIYUAN_IMAGE_TAR)
	tar -xzvf ./merges/$(SIYUAN_IMAGE_TAR) -C ./merges
	$(call ls_images)

load:
	# docker image rm $(SIYUAN_IMAGE)
	docker load -i ./merges/$(SIYUAN_IMAGE_SAVE) 

clean:
	docker image rm $(SIYUAN_IMAGE)
	rm -rf ./splits/* ./merges/*
	$(call ls_images)
	
ls:
	$(call ls_images)

start:
	docker run \
	-v /wine/siyuan:/siyuan/workspace \
	-p 6806:6806 \
	-u 1000:1000 \
	$(SIYUAN_IMAGE) \
	--lang=zh_CN \
	--workspace=/siyuan/workspace \
	--accessAuthCode=123


