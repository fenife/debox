package entity

import "server-go/domain/do"

type Category struct {
	BaseModel

	Name string `gorm:"type:varchar(255);not null;unique;comment:'分类名称'" json:"name"`
}

func (c *Category) IsValid() bool {
	// 未删除，且id>0
	return c.DeletedAt.Valid == false && c.ID > 0
}

func (c *Category) ToTiny() *do.CategoryTiny {
	if c == nil {
		return nil
	}
	newCate := do.CategoryTiny{
		ID:   c.ID,
		Name: c.Name,
	}
	return &newCate
}

func (c *Category) ToSmall() *do.CategorySmall {
	if c == nil {
		return nil
	}
	newCate := do.CategorySmall{
		ID:        c.ID,
		CreatedAt: c.CreatedAt.Format(timeFormatLayout),
		UpdatedAt: c.CreatedAt.Format(timeFormatLayout),
		Name:      c.Name,
	}
	return &newCate
}
