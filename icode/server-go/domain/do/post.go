package do

type PostStat struct {
	CateId    uint64 `json:"cate_id"`
	PostCount int    `json:"post_count"`
}

type PostSmall struct {
	ID        uint64 `json:"id"`
	CreatedAt string `json:"created_at"` // "2006-01-02 15:05:05"
	UpdatedAt string `json:"updated_at"` // 同上
	UserId    uint64 `json:"user_id"`
	CateId    uint64 `json:"cate_id"`
	Title     string `json:"title"`
	TitleEn   string `json:"title_en"`
}

type PostDetail struct {
	PostSmall
	Content  string        `json:"content"` // 文章详情
	User     *UserTiny     `json:"user"`
	Category *CategoryTiny `json:"category"`
}
