package resp

import (
	"server-go/application/dto"
	"server-go/domain/do"
)

type PostListResp struct {
	Total    int              `json:"total"`
	PostList []*do.PostDetail `json:"post_list"`
}

type PostDetailResp struct {
	*dto.PostDetailWithPreNext
}

type PostArchiveResp struct {
	List []*dto.PostArchiveItem `json:"list"`
}
