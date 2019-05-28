# Particle Filter

I will do this in Golang eventually for visualizing the resampling procedure.

```golang
package main

import (
    "fmt"
    "time"

    "golang.org/x/exp/rand"

    "gonum.org/v1/gonum/stat/sampleuv"
)

func main() {
    samples := []string{"hello", "world", "what's", "going", "on?"}
    weights := []float64{1.0, 0.55, 1.23, 1, 0.002}

    w := sampleuv.NewWeighted(
        weights,
        rand.New(rand.NewSource(uint64(time.Now().UnixNano())))
    )

    i, _ := w.Take()

    fmt.Println(samples[i])
}
```