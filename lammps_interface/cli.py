#!/usr/bin/env python
import sys
from .lammps_main import LammpsSimulation
from .structure_data import ase_from_CIF, from_CIF, write_CIF, write_PDB, write_RASPA_CIF, write_RASPA_sim_files, MDMC_config
from .InputHandler import Options

def main():
    print("开始解析命令行参数...")
    options = Options()
    
    print("初始化 LammpsSimulation...")
    sim = LammpsSimulation(options)
    
    print("从 CIF 文件读取结构...")
    cell, graph = from_CIF(options.cif_file)
    #cell, graph = ase_from_CIF(options.cif_file)
    
    print("设置晶胞参数...")
    sim.set_cell(cell)
    
    print("设置分子图...")
    sim.set_graph(graph)
    
    print("分割分子图...")
    sim.split_graph()
    
    print("分配力场参数...")
    sim.assign_force_fields()
    
    print("计算模拟尺寸...")
    sim.compute_simulation_size()
    
    print("合并分子图...")
    sim.merge_graphs()
    
    if options.output_cif:
        print("正在生成 CIF 文件...")
        write_CIF(graph, cell)
        sys.exit()
        
    if options.output_pdb:
        print("正在生成 PDB 文件...")
        write_PDB(graph, cell)
        sys.exit()
        
    print("正在写入 LAMMPS 文件...")
    sim.write_lammps_files()

    if options.output_raspa:
        print("正在生成 RASPA 文件...")
        classifier = 1
        write_RASPA_CIF(graph, cell, classifier)
        write_RASPA_sim_files(sim, classifier)
        this_config = MDMC_config(sim)
        sim.set_MDMC_config(this_config)
