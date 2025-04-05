package resp

import "server-go/application/dto"

type CategoryListResp struct {
	Total    int                    `json:"total"` // 文章分类的总数目
	CateList []dto.CategoryListItem `json:"cate_list"`
}
