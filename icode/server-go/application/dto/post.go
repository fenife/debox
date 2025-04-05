package dto

import "server-go/domain/do"

type PostArchiveItem struct {
	Year     int              `json:"year"`      // 创建年份
	Count    int              `json:"count"`     // 文章数目
	PostList []*do.PostDetail `json:"post_list"` // 文章列表，文章内容为""，不需要展示
}

type PostDetail struct {
	*do.PostDetail
	Toc string `json:"toc"` // markdown的目录
}

type PostDetailWithPreNext struct {
	Post *PostDetail    `json:"post"`
	Pre  *do.PostDetail `json:"pre"`
	Next *do.PostDetail `json:"next"`
}
