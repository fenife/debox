/*
Data Transfer Object (dto)
一个领域(domain)里的对象可以用 entity 或者 do 里的对象表示；
当涉及多个领域的数据，需要进行聚合时，可以在 dto 里定义
*/

package dto

import "server-go/domain/do"

type CategoryListItem struct {
	*do.CategoryTiny
	PostCount int `json:"post_count"` // 该分类下的文章数
}
