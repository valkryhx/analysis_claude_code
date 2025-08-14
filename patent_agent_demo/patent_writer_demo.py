#!/usr/bin/env python3
"""
专利撰写演示脚本
使用 GLM-4.5-flash 模型自动撰写专利文档
"""

import asyncio
import sys
import os
from typing import Dict, Any, List
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import config
from glm_client import GLMClient, PatentDraft, PatentAnalysis

console = Console()

class PatentWriterDemo:
    """专利撰写演示类"""
    
    def __init__(self):
        self.glm_client = None
        self.current_patent = None
        
    async def start(self):
        """启动专利撰写演示"""
        try:
            console.print(Panel.fit(
                "[bold blue]专利撰写演示系统[/bold blue]\n"
                "基于 GLM-4.5-flash 的智能专利撰写平台\n"
                "Powered by Zhipu AI",
                border_style="blue"
            ))
            
            # 验证配置
            if not config.validate_config():
                console.print("[red]❌ 配置验证失败，请检查 API key[/red]")
                return
            
            # 初始化 GLM 客户端
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("初始化 GLM 客户端...", total=None)
                
                self.glm_client = GLMClient(config.get_glm_api_key())
                
                progress.update(task, description="GLM 客户端初始化成功!")
            
            console.print("[green]✅ 系统启动成功![/green]")
            
            # 显示主菜单
            await self.show_main_menu()
            
        except Exception as e:
            console.print(f"[red]❌ 启动失败: {e}[/red]")
            raise
    
    async def show_main_menu(self):
        """显示主菜单"""
        while True:
            console.print("\n" + "="*60)
            console.print("[bold cyan]主菜单[/bold cyan]")
            console.print("1. 📋 专利主题分析")
            console.print("2. ✍️  撰写专利文档")
            console.print("3. 🔍 专利检索分析")
            console.print("4. 📊 专利性评估")
            console.print("5. 💾 保存专利文档")
            console.print("6. 📁 查看已保存专利")
            console.print("0. 🚪 退出系统")
            
            choice = Prompt.ask("请选择功能", choices=["0", "1", "2", "3", "4", "5", "6"])
            
            if choice == "0":
                console.print("[yellow]👋 感谢使用专利撰写系统![/yellow]")
                break
            elif choice == "1":
                await self.analyze_patent_topic()
            elif choice == "2":
                await self.draft_patent()
            elif choice == "3":
                await self.search_patents()
            elif choice == "4":
                await self.assess_patentability()
            elif choice == "5":
                await self.save_patent()
            elif choice == "6":
                await self.view_saved_patents()
    
    async def analyze_patent_topic(self):
        """专利主题分析"""
        console.print("\n[bold green]📋 专利主题分析[/bold green]")
        
        topic = Prompt.ask("请输入专利主题")
        description = Prompt.ask("请输入专利描述")
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("正在分析专利主题...", total=None)
                
                analysis = await self.glm_client.analyze_patent_topic(topic, description)
                
                progress.update(task, description="分析完成!")
            
            # 显示分析结果
            table = Table(title="专利分析结果")
            table.add_column("评估项目", style="cyan")
            table.add_column("结果", style="green")
            
            table.add_row("新颖性评分", f"{analysis.novelty_score}/10")
            table.add_row("创造性评分", f"{analysis.inventive_step_score}/10")
            table.add_row("工业实用性", "✅" if analysis.industrial_applicability else "❌")
            table.add_row("专利性评估", analysis.patentability_assessment)
            
            console.print(table)
            
            # 显示建议
            console.print("\n[bold yellow]💡 改进建议:[/bold yellow]")
            for i, rec in enumerate(analysis.recommendations, 1):
                console.print(f"{i}. {rec}")
            
            # 询问是否继续撰写
            if Confirm.ask("是否基于此分析结果撰写专利文档?"):
                self.current_patent = {
                    'topic': topic,
                    'description': description,
                    'analysis': analysis
                }
                await self.draft_patent()
                
        except Exception as e:
            console.print(f"[red]❌ 分析失败: {e}[/red]")
    
    async def draft_patent(self):
        """撰写专利文档"""
        console.print("\n[bold green]✍️  撰写专利文档[/bold green]")
        
        if not self.current_patent:
            topic = Prompt.ask("请输入专利主题")
            description = Prompt.ask("请输入专利描述")
        else:
            topic = self.current_patent['topic']
            description = self.current_patent['description']
            console.print(f"使用已分析的主题: {topic}")
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("正在撰写专利文档...", total=None)
                
                draft = await self.glm_client.draft_patent(topic, description)
                
                progress.update(task, description="撰写完成!")
            
            # 显示专利草稿
            console.print("\n[bold green]📄 专利草稿[/bold green]")
            console.print(f"[bold]标题:[/bold] {draft.title}")
            console.print(f"[bold]摘要:[/bold] {draft.abstract}")
            console.print(f"[bold]背景技术:[/bold] {draft.background[:200]}...")
            console.print(f"[bold]发明内容:[/bold] {draft.summary[:200]}...")
            console.print(f"[bold]权利要求数量:[/bold] {len(draft.claims)}")
            
            # 显示权利要求
            console.print("\n[bold yellow]权利要求:[/bold yellow]")
            for i, claim in enumerate(draft.claims, 1):
                console.print(f"{i}. {claim[:100]}...")
            
            # 保存到当前专利
            self.current_patent = {
                'topic': topic,
                'description': description,
                'draft': draft
            }
            
            console.print("\n[green]✅ 专利文档撰写完成![/green]")
            
        except Exception as e:
            console.print(f"[red]❌ 撰写失败: {e}[/red]")
    
    async def search_patents(self):
        """专利检索分析"""
        console.print("\n[bold green]🔍 专利检索分析[/bold green]")
        console.print("[yellow]此功能需要集成专利数据库，当前版本暂未实现[/yellow]")
    
    async def assess_patentability(self):
        """专利性评估"""
        console.print("\n[bold green]📊 专利性评估[/bold green]")
        
        if not self.current_patent or 'draft' not in self.current_patent:
            console.print("[yellow]请先撰写专利文档[/yellow]")
            return
        
        try:
            draft = self.current_patent['draft']
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("正在评估专利性...", total=None)
                
                # 使用 GLM 进行专利性评估
                prompt = f"""
                请评估以下专利的专利性:
                
                标题: {draft.title}
                摘要: {draft.abstract}
                权利要求: {chr(10).join(draft.claims)}
                
                请从以下方面进行评估:
                1. 新颖性 (0-10分)
                2. 创造性 (0-10分)  
                3. 工业实用性
                4. 整体专利性评估
                5. 改进建议
                """
                
                assessment = await self.glm_client.generate_response(prompt)
                
                progress.update(task, description="评估完成!")
            
            console.print("\n[bold green]📊 专利性评估结果[/bold green]")
            console.print(assessment)
            
        except Exception as e:
            console.print(f"[red]❌ 评估失败: {e}[/red]")
    
    async def save_patent(self):
        """保存专利文档"""
        console.print("\n[bold green]💾 保存专利文档[/bold green]")
        
        if not self.current_patent or 'draft' not in self.current_patent:
            console.print("[yellow]没有可保存的专利文档[/yellow]")
            return
        
        try:
            filename = Prompt.ask("请输入保存文件名", default="patent_draft.txt")
            
            draft = self.current_patent['draft']
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"专利标题: {draft.title}\n")
                f.write(f"专利摘要: {draft.abstract}\n")
                f.write(f"背景技术: {draft.background}\n")
                f.write(f"发明内容: {draft.summary}\n")
                f.write(f"详细描述: {draft.detailed_description}\n")
                f.write("\n权利要求:\n")
                for i, claim in enumerate(draft.claims, 1):
                    f.write(f"{i}. {claim}\n")
                f.write(f"\n附图说明: {draft.drawings_description}\n")
            
            console.print(f"[green]✅ 专利文档已保存到 {filename}[/green]")
            
        except Exception as e:
            console.print(f"[red]❌ 保存失败: {e}[/red]")
    
    async def view_saved_patents(self):
        """查看已保存专利"""
        console.print("\n[bold green]📁 查看已保存专利[/bold green]")
        console.print("[yellow]此功能需要实现专利存储系统，当前版本暂未实现[/yellow]")


async def main():
    """主函数"""
    demo = PatentWriterDemo()
    await demo.start()


if __name__ == "__main__":
    asyncio.run(main())