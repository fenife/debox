
include $(INC_DIR)/Makefile.common

ORIGIN_IMAGE=registry.access.redhat.com/ubi8/ubi:8.4-213
IMAGE=ubi8:8.4
IMAGE_SAVE=ubi-8.4.tar
IMAGE_TAR=ubi-8.4.tar.gz

pull:
	docker pull $(ORIGIN_IMAGE)

tag:
	docker tag $(ORIGIN_IMAGE) $(IMAGE)

# pull:
# 	# docker pull m.daocloud.io/docker.io/$(IMAGE)

# tag:
# 	docker tag m.daocloud.io/docker.io/$(IMAGE) $(IMAGE)

save: 
	mkdir -p ./saves/
	if [ -f ./saves/${IMAGE_SAVE} ]; then rm ./saves/${IMAGE_SAVE}; fi
	docker save -o ./saves/${IMAGE_SAVE} ${IMAGE}

tar:
	tar -czvf ./saves/$(IMAGE_TAR) ./saves/$(IMAGE_SAVE)

define ls_images
	@echo
	ls -alh ./saves
	@echo
	ls -alh ./splits
	@echo
	ls -alh ./merges
	@echo
	docker image ls | grep ubi
endef

# -b 3G 表示设置每个分割包的大小，单位还是可以m,k
# -d "参数指定生成的分割包后缀为数字的形式
# -a x来设定序列的长度(默认值是2)，这里设定序列的长度为1
split:
	mkdir -p ./splits
	split -b 9m -d -a 1 ./saves/$(IMAGE_TAR) ./splits/$(IMAGE_TAR).
	$(call ls_images)

merge:
	rm -rf ./merges
	mkdir -p ./merges
	cat ./splits/$(IMAGE_TAR).* > ./merges/$(IMAGE_TAR)
	tar -xzvf ./merges/$(IMAGE_TAR) -C ./merges
	$(call ls_images)

load:
	docker image rm $(IMAGE)
	docker load -i ./merges/saves/$(IMAGE_SAVE) 
	$(call ls_images)

clean:
	-docker image rm $(IMAGE)
	-rm -rf ./saves ./splits ./merges
	$(call ls_images)
	
ls:
	$(call ls_images)

check:
	docker run --rm -it $(IMAGE) 


## split
# pull tag save tar split merge load clean 
## merge
# upload file to ./splits
# merge load clean 


