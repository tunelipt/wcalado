
require(XMLRPC)


roboDev <- function(ip="localhost", port=9595){
    add <- paste0(ip, ":", port)
    dev <- list(add=add, ip=ip, port=port)
    class(dev) <- "robo"
    return(dev)
}
mesaDev <- function(ip="localhost", port=9596){
    add <- paste0(ip, ":", port)
    dev <- list(add=add, ip=ip, port=port)
    class(dev) <- "mesa"
    return(dev)
}
    
move <- function(absdev, ...) UseMethod("move", absdev)
moveX <- function(absdev, ...) UseMethod("moveX", absdev)
moveY <- function(absdev, ...) UseMethod("moveY", absdev)
moveZ <- function(absdev, ...) UseMethod("moveZ", absdev)

rmove <- function(absdev, ...) UseMethod("rmove", absdev)
rmoveX <- function(absdev, ...) UseMethod("rmoveX", absdev)
rmoveY <- function(absdev, ...) UseMethod("rmoveY", absdev)
rmoveZ <- function(absdev, ...) UseMethod("rmoveZ", absdev)

absPosition <- function(absdev, ...) UseMethod("absPosition", absdev)
position <- function(absdev, ...) UseMethod("position", absdev)
setReference <- function(absdev, ...) UseMethod("setReference", absdev)
setAbsReference <- function(absdev, ...) UseMethod("setAbsReference", absdev)
home <- function(absdev, ...) UseMethod("home", absdev)
stopDev <- function(absdev, ...) UseMethod("stopDev", absdev)
clearDev <- function(absdev, ...) UseMethod("clearDev", absdev)
waitUntilDone <- function(absdev, ...) UseMethod("waitUntilDone", absdev)

move.robo <- function(dev, x='', y='', z='', a=FALSE, r=FALSE, sync=FALSE){
    xml.rpc(dev$add, "move", x, y, z, a, r, sync)
}
moveX.robo <- function(dev, x='', a=FALSE, r=FALSE, sync=FALSE){
    xml.rpc(dev$add, "move", x, '', '', a, r, sync)
}
moveY.robo <- function(dev, y='', a=FALSE, r=FALSE, sync=FALSE){
    xml.rpc(dev$add, "move", '', y, '', a, r, sync)
}
moveZ.robo <- function(dev, z='', a=FALSE, r=FALSE, sync=FALSE){
    xml.rpc(dev$add, "move", '', '', z, a, r, sync)
}

rmove.robo <- function(dev, x='', y='', z='', sync=FALSE){
    xml.rpc(dev$add, "rmove", x, y, z, sync)
}

rmoveX.robo <- function(dev, x='', sync=FALSE){
    xml.rpc(dev$add, "rmove", x, '', '', sync)
}
rmoveY.robo <- function(dev, y='', sync=FALSE){
    xml.rpc(dev$add, "rmove", '', y, '', sync)
}
rmoveZ.robo <- function(dev, z='', sync=FALSE){
    xml.rpc(dev$add, "rmove", '', '', z, sync)
}

absPosition.robo <- function(dev){
    xml.rpc(dev$add, "abs_position")
}
position.robo <- function(dev){
    xml.rpc(dev$add, "position")
}


setReference.robo <- function(dev, eixo=''){
    xml.rpc(dev$add, "set_reference", eixo)
}
setAbsReference.robo <- function(dev){
    xml.rpc(dev$add, "set_abs_reference")
}

home.robo <- function(dev, eixo='z', sinal='+'){
    xml.rpc(dev$add, "home", eixo, sinal)
}

stopDev.robo <- function(dev){
    xml.rpc(dev$add, "stop")
}

clearDev.robo <- function(dev){
    xml.rpc(dev$add, "clear")
}

waitUntilDone.robo <- function(dev){
    xml.rpc(dev$add, "waitUntilDone")
}


move.mesa <- function(dev, x, a=FALSE, r=FALSE, sync=FALSE){
    xml.rpc(dev$add, "move", x, a, r, sync)
}
moveX.mesa <- function(dev, x, a=FALSE, r=FALSE, sync=FALSE){
    xml.rpc(dev$add, "move", x, a, r, sync)
}

rmove.mesa <- function(dev, x, sync=FALSE){
    xml.rpc(dev$add, "rmove", x, sync)
}

rmoveX.mesa <- function(dev, x, sync=FALSE){
    xml.rpc(dev$add, "rmove", x, sync)
}

absPosition.mesa <- function(dev, pulses=FALSE){
    xml.rpc(dev$add, "abs_position", pulses)
}
position.mesa <- function(dev){
    xml.rpc(dev$add, "position")
}


setReference.mesa <- function(dev){
    xml.rpc(dev$add, "set_reference")
}
setAbsReference.mesa <- function(dev){
    xml.rpc(dev$add, "set_abs_reference")
}

home.mesa <- function(dev, sinal='-'){
    xml.rpc(dev$add, "home", sinal, sinal)
}

stopDev.mesa <- function(dev){
    xml.rpc(dev$add, "stop")
}

clearDev.mesa <- function(dev){
    xml.rpc(dev$add, "clear")
}

waitUntilDone.mesa <- function(dev){
    xml.rpc(dev$add, "waitUntilDone")
}

