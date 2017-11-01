effect_col = colors()[75]
vals = c(bzx-bzx_se, bzx+bzx_se)
xmin = min(vals); xmax = max(vals)
vals = c(bzy-bzy_se, bzy+bzy_se)
ymin = min(vals); ymax = max(vals)
par(mar=c(5,5,4,2))
plot(bzx, bzy, pch=20, cex=0.8, bty="n", cex.axis=1.1, cex.lab=1.2,
             col=effect_col, xlim=c(xmin, xmax), ylim=c(ymin, ymax),
                     xlab=expression(LDL~cholesterol~(italic(b[zx]))),
                             ylab=expression(Coronary~artery~disease~(italic(b[zy]))))
abline(0, gsmr_results$bxy, lwd=1.5, lty=2, col="dim grey")

nsnps = length(bzx)
for( i in 1:nsnps ) {
        # x axis
        xstart = bzx[i] - bzx_se[i]; xend = bzx[i] + bzx_se[i]
    ystart = bzy[i]; yend = bzy[i]
        segments(xstart, ystart, xend, yend, lwd=1.5, col=effect_col)
        # y axis
        xstart = bzx[i]; xend = bzx[i] 
            ystart = bzy[i] - bzy_se[i]; yend = bzy[i] + bzy_se[i]
            segments(xstart, ystart, xend, yend, lwd=1.5, col=effect_col)
}
