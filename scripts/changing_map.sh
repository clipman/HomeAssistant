#!/bin/bash

set -e

declare fePath
declare -a searchingPaths=(
	"/usr/local/lib/"
	"/root/homeassistant/lib/"
	"/var/lib/docker/overlay2"
)

function info () { echo -e "INFO: $1";}
function warn () { echo -e "WARN: $1";}
function error () { echo -e "ERROR: $1"; if [ "$2" != "false" ]; then exit 1;fi; }

function checkRequirement () {
	if [ -z "$(command -v "$1")" ]; then
		error "'$1' 가 설치되어 있지 않습니다."
	fi
}

checkRequirement "wget"

for searchingPath in "${searchingPaths[@]}"; do
	if [ -n "$fePath" ]; then
		break
	fi

	# info "'$searchingPath' 에서 hass_frontend 디렉토리 찾는중..."

	findPaths=($(find $searchingPath -name hass_frontend -type d))
	findCnt=${#findPaths[@]}

	if [ $findCnt -gt 0 ]; then
		# echo "* 작업 대상 경로 목록"
		for (( n = 0; n < $findCnt; n++ )); do
			echo -e "    $(expr $n + 1)) ${findPaths[$n]}"
                        fePath=${findPaths[$n]}
		done

		if [ -n "$fePath" ]; then
			info "'$fePath 에서 패치 진행..."
		else
			error "패치를 수행할 hass_frontend 경로를 찾지 못하였습니다."
		fi
		
		cd $fePath
		
		cur_dir=${PWD##*/}
		
		# if [ $cur_dir != 'hass_frontend' ]; then
		# 	error "작업 경로가 올바르지 않습니다. 'hass_frontend'!! ('$cur_dir')"
		# fi
		
		declare ES5_TARGET_FILES=($(grep -nrl 'basemaps.cartocdn.com' ./frontend_es5/*.js))
		
		# info "frontend_es5/ 디렉토리 패치중.."
		for targetFile in "${ES5_TARGET_FILES[@]}"; do
			echo -e "  patch file : $targetFile"
			cp $targetFile ${targetFile}.backup
		        sed -i 's/\"https:\/\/basemaps.cartocdn.com\/.*maxZoom:20/\"https:\/\/map.pstatic.net\/nrb\/styles\/basic\/\{z\}\/\{x\}\/\{y\}\.png\?mt\=bg\.ol\.ts\.ar\.lko"\,\{minZoom:6,maxZoom:19/g' $targetFile
			gzip -f -k $targetFile
		done
		
		if [ ${#ES5_TARGET_FILES[@]} -eq 0 ]; then
			info "frontend_es5/ 디렉토리에 패치할 파일이 없습니다."
		fi
		
		declare LATEST_TARGET_FILES=($(grep -nrl 'basemaps.cartocdn.com' ./frontend_latest/*.js))
		
		# info "frontend_latest/ 디렉토리 패치중.."
		for targetFile in "${LATEST_TARGET_FILES[@]}"; do
			echo -e "  patch file : $targetFile"
			cp $targetFile ${targetFile}.backup
		        sed -i 's/\"https:\/\/basemaps.cartocdn.com\/.*maxZoom:20/\"https:\/\/map.pstatic.net\/nrb\/styles\/basic\/\{z\}\/\{x\}\/\{y\}\.png\?mt\=bg\.ol\.ts\.ar\.lko"\,\{minZoom:6,maxZoom:19/g' $targetFile
			gzip -f -k $targetFile
		done
		
		
		if [ ${#LATEST_TARGET_FILES[@]} -eq 0 ]; then
			info "frontend_latest/ 디렉토리에 패치할 파일이 없습니다."
		fi
	fi
done

info "작업 완료!!"
