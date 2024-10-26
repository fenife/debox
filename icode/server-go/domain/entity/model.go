package entity

import (
	"gorm.io/gorm"
	"time"
)

const timeFormatLayout = "2006-01-02 15:05:05"

type BaseModel struct {
	ID        uint64         `gorm:"type:bigint;not null;primary_key;auto_increment" json:"id"`
	CreatedAt time.Time      `gorm:"type:datetime;not null;default:CURRENT_TIMESTAMP" json:"created_at"`
	UpdatedAt time.Time      `gorm:"type:datetime;not null;default:CURRENT_TIMESTAMP" json:"updated_at"`
	DeletedAt gorm.DeletedAt `gorm:"type:datetime;null;index" json:"deleted_at"`
}
