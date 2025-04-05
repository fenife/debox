package req

type GetPostListReq struct {
	CateId uint64 `form:"cate_id" binding:"omitempty,gte=1"` // 分类id
	Page   int    `form:"page" binding:"omitempty,gte=1"`
	Limit  int    `form:"limit" binding:"omitempty,gte=1"`
}

type GetPostDetailReq struct {
	PostId      uint64 `form:"post_id" binding:"required"`           // 文章id
	ContentType string `form:"ct" binding:"omitempty,oneof=html md"` // 文章内容类型，html或者markdown
}

type GetPostArchiveReq struct {
}

type GetPostAboutReq struct {
	ContentType string `form:"ct" binding:"omitempty,oneof=html md"`
}

type SearchPostReq struct {
	KeyWord string `form:"kw" binding:"required"` // 搜索关键字
	Page    int    `form:"page" binding:"omitempty,gte=1"`
	Limit   int    `form:"limit" binding:"omitempty,gte=1"`
}

type CreatePostReq struct {
	UserId  uint64 `json:"user_id" binding:"required,gte=1"`
	CateId  uint64 `json:"cate_id" binding:"required,gte=1"`
	Title   string `json:"title" binding:"required"`
	TitleEn string `json:"title_en" binding:"required"`
	Content string `json:"content" binding:"required"`
}
