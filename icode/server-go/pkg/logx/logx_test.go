package logx

import (
	"context"
	"testing"
)

func TestLog(t *testing.T) {

	Debugf("t1")

	ctx := context.Background()
	Ctx(ctx).Infof("t2")

	Ctx(ctx).With("a", 1).With("b", 2).Warnf("t3")
	Ctx(ctx).With("a", 1, "b", 2).Warnf("t4")

	ctx = context.WithValue(ctx, keyReqId, "req-id-123")
	ctx = context.WithValue(ctx, keyTraceId, "trace-id-123")
	l := Ctx(ctx).With("a", 2)
	l.Infof("t5")
	l.With("b", 3).Warnf("t6")

	Debugf("t7 %d", 1)
	Ctx(ctx).Infof("t8 %d", 2)
	Warnf("t9 %d", 3)
	With("t10", "a").Infof("")
	Infof("", 1, "a", "b")
	Infof("", 1, 2)
	Errorf("t12 %d %d %d", 1, 2, 3)
}
