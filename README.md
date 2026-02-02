# 由俺尋思之力驅動 (* ￣︿￣)

## 前置依赖
- Git
- Python interpreter 3.12
- Nim Compiler 
- CMake
- Windows 10 SDK 或 Windows 11 SDK
- MSVC v142 - VS 2019 C++ x64/x86 Build Tool

## 構建
- 使用管理員權限運行 [`./build.cmd`](build.cmd)


## 內存讀取模式
- ### `meow` （[qb-0/pyMeow](https://github.com/qb-0/pyMeow)）
  - 基於 [Windows API](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-readprocessmemory) 的內存讀寫
- ### `neac` （[za233/NeacController](https://github.com/za233/NeacController)）
  - 基於 [NeacSafe64.sys 驅動漏洞](https://nvd.nist.gov/vuln/detail/CVE-2025-45737) 的內存讀寫
  - [Process](https://learn.microsoft.com/zh-cn/windows/win32/toolhelp/taking-a-snapshot-and-viewing-processes) 與 [Module](https://learn.microsoft.com/zh-cn/windows/win32/toolhelp/traversing-the-module-list) 的讀取依然使用 Windows API
- ### `fpga` （[ufrisk/MemProcFS](https://github.com/ufrisk/MemProcFS)）
  - 基於 [DMA](https://en.wikipedia.org/wiki/Direct_memory_access) 等 [FPGA](https://github.com/ufrisk/pcileech/) 硬體設備的內存讀寫