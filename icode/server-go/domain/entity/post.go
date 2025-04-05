package entity

import "server-go/domain/do"

type Post struct {
	BaseModel

	UserId  uint64 `gorm:"type:bigint;index;not null;comment:'用户id'" json:"user_id"`
	CateId  uint64 `gorm:"type:bigint;index;not null;comment:'分类id'" json:"cate_id"`
	Title   string `gorm:"type:varchar(255);not null;unique;comment:'中文标题'" json:"title"`
	TitleEn string `gorm:"type:varchar(255);not null;unique;comment:'英文标题'" json:"title_en"`
	Content string `gorm:"type:text;not null;comment:'文章内容'" json:"content"`

	User     User     `gorm:"foreignKey:UserId"`
	Category Category `gorm:"foreignKey:CateId"`
}

func (p *Post) IsValid() bool {
	// 未删除，且id>0
	return p.DeletedAt.Valid == false && p.ID > 0
}

func (p *Post) ToSmall() *do.PostSmall {
	if p == nil {
		return nil
	}
	newPost := do.PostSmall{
		ID:        p.ID,
		CreatedAt: p.CreatedAt.Format(timeFormatLayout),
		UpdatedAt: p.CreatedAt.Format(timeFormatLayout),
		UserId:    p.UserId,
		CateId:    p.CateId,
		Title:     p.Title,
		TitleEn:   p.TitleEn,
	}
	return &newPost
}

func (p *Post) ToDetail() *do.PostDetail {
	if p == nil {
		return nil
	}
	detail := do.PostDetail{
		PostSmall: *p.ToSmall(),
		User:      p.User.ToTiny(),
		Category:  p.Category.ToTiny(),
	}
	//detail.Content = p.Content
	return &detail
}
