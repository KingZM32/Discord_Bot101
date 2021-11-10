from discord.ext import commands
from .todolist_templates import help_template, list_template
import os
import json
 
#TODO: Gerenciar uma todo list para um dado membro
# FEATURES --
# .> Acrescentar / Remover tarefas
# .> Verificar tarefas pendentes
#TODO: bridge todo_list object <--> dictionary

here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here, 'stored_tasks.json') 

try:
    with open(filename) as file:
        stored_tasks = json.load(file)
except FileNotFoundError:
    stored_tasks = {}

# Dump new values
def dump():
    global here, filename
    with open(filename, "w") as file:
        json.dump(stored_tasks, file)

# Instantiate a todo-list object
def instantiate_list(member_id, param):
    return todo(
        member_id, 
        param
        )

class todo():

    def __init__(self, member, param): 
        self.member = member 
        self.param = param

    # Add task to user's list 
    async def add_task(self):
        if self.member not in stored_tasks:
            stored_tasks[self.member] = {}
            stored_tasks[self.member][1] = self.param
        else:
            tasks_amount = len(stored_tasks[self.member])
            index = tasks_amount + 1
            stored_tasks[self.member][index] = self.param

    # Remove task from user's list
    async def remove_task(self):
        index = self.param
        tasks_amount = len(stored_tasks[self.member])

        del stored_tasks[self.member][index] 
        
        post_index = self.param + 1
        self.update_indexes(post_index, tasks_amount)

    # Complete a given task <-> param = num
    async def complete_task(self) -> str:
        index = self.param
        task = stored_tasks[self.member][index]
        tasks_amount = len(stored_tasks[self.member])

        del stored_tasks[self.member][index] 
        
        post_index = self.param + 1
        self.update_indexes(post_index, tasks_amount)

        return task 

    # Update dict entries after a given action
    def update_indexes(self, post_index, tasks_amount):
        for i in range(post_index, tasks_amount + 1):
            current_task = stored_tasks[self.member][i]
            stored_tasks[self.member][i-1] = current_task
            del stored_tasks[self.member][i]  


class todolist(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.group(name="todo")
    async def todo(self, ctx):
        channel = ctx.channel
        
        # Main command <--> Todo-list template
        if ctx.invoked_subcommand is None:
            member = ctx.author.id 
            
            if member not in stored_tasks or not bool(stored_tasks[member]):
                emb = help_template()
                await channel.send(embed = emb)
                return
            
            emb = list_template(ctx.author.display_name, stored_tasks[member])
            await channel.send(embed=emb)
    
    @todo.command(name = "add", aliases = ["a"])
    async def add(self, ctx, *, task):
        member = ctx.author.id
        channel = ctx.channel
        
        # Verificar se há tarefa
        if len(task) < 3:
            await channel.send("Please insert a valid <task>")
            return 

        user_list = instantiate_list(member, task)
        # Add user's task
        await user_list.add_task()
        await ctx.send("{}\nTask: «{}» has been added to your to-do list.".format(ctx.author.mention, task))
        dump()

    @todo.command(name = "remove", aliases = ["delete", "rm", "del"])
    async def remove(self, ctx, num=None):
        member = ctx.author.id
        num = int(num)

        # Check if user has a prompted <num>
        if num is None:
            await ctx.send("Please insert a specific <task_num>")

        # Check if user has a submitted task
        if member not in stored_tasks:
            await ctx.author.send("The prompted task doesn't exist. Are you sure you inserted the right task number?") 
            return 
        
        # Check if given task number is valid
        amount = len(stored_tasks[member])
        if num not in range(1, amount + 1):
            await ctx.author.send("That task doesn't exist. You have {} active tasks.".format(amount))
            return

        # Remove task and update list
        user_list = instantiate_list(member, num)
        await user_list.remove_task()
        await ctx.send("{}\nTask {} has been removed from your to-do list.".format(ctx.author.mention, num))
        dump()

    @todo.command(name = "done", aliases = ["complete", "d"])
    async def complete(self, ctx, num):
        member = ctx.author.id
        num = int(num)

        # Check if user has a prompted <num>
        if num is None:
            await ctx.send("Please insert a specific <task_num>")

        # Check if user has a submitted task
        if member not in stored_tasks:
            await ctx.author.send("The prompted task doesn't exist. Are you sure you inserted the right task number?") 
            return 
        
        # Check if given task number is valid
        amount = len(stored_tasks[member])
        if num not in range(1, amount + 1):
            await ctx.author.send("That task doesn't exist. You have {} active tasks.".format(amount))
            return

        user_list = instantiate_list(member, num)

        # Complete task and update list
        task_str = await user_list.complete_task() 
        await ctx.send("Well done, {}.\nTask {}: «{}» has been completed.".format(ctx.author.mention, num, task_str))
        dump()
        
def setup(client):
    client.add_cog(todolist(client))
    


