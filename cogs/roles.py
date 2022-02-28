import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument, MissingPermissions

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tick = '<:tick:879670104000954400>'
        self.cross = '<:Cross:879670127707193364>'

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} is ready!')

    @commands.command(aliases=['newr'])
    @commands.has_permissions(manage_roles=True)
    async def newrole(self, ctx, hex='ffffff', *, role_name=None):
        """Creates a role for the server"""
        if not role_name:
            return await ctx.send(f'{self.cross} Please enter a role name')
        if role_name in [str(r.name) for r in ctx.guild.roles]:
            return await ctx.send(f"{self.cross} **Role already exists!**")
        try:
            role = await ctx.guild.create_role(name=role_name, color=discord.Color(int(hex)))
        except discord.Forbidden:
            return await ctx.send(f"{self.cross} **I don't have permission to create roles!**")
        except discord.HTTPException:
            return await ctx.send(f"{self.cross} **Something went wrong!**")
        except discord.InvalidArgument:
            return await ctx.send(f"{self.cross} **Invalid argument!**")
        em = discord.Embed(
            title = f"{self.tick} Role created!",
            description = f"{role.mention}\nRole name: `{role.name}`\nRole ID: `{role.id}`",
            color = discord.Color.yellow()
        )
        await ctx.send(embed=em)

    @commands.command(aliases=['deleterole', 'delr'])
    @commands.has_permissions(manage_roles=True)
    async def delrole(self, ctx, *, role_name = None):
        """Deletes role"""
        if not role_name:
            return await ctx.send(f"{self.cross} **Please specify a role!**")
        if role_name not in [str(r.name) for r in ctx.guild.roles]:
            await ctx.send(f"{self.cross} **Role doesn't exist!**")
        else:
            try:
                role = discord.utils.get(ctx.guild.roles, name=role_name)
            except:
                return await ctx.send(f"{self.cross} **No such role!**")
            try:
                await role.delete()
            except discord.Forbidden:
                return await ctx.send(f"{self.cross} **I don't have permission to delete roles!**")
            except discord.HTTPException:
                return await ctx.send(f"{self.cross} **Something went wrong!**")

            em = discord.Embed(
                title = f"{self.tick} Role deleted!",
                description = f"Role `{role.name}` has been successfully deleted.",
                color = discord.Color.yellow()
            )
            await ctx.send(embed=em)

    @commands.command(aliases=['giver'])
    @commands.has_permissions(manage_roles=True)
    async def giverole(self, ctx, role , member : discord.Member):
        """Gives role to a member"""
        role = discord.utils.get(ctx.guild.roles, name=role)
        if role in member.roles:
            return await ctx.send(f"**{self.cross} {member} already has {role} role**")
        try:
            await member.add_roles(role)
        except discord.Forbidden:
            return await ctx.send(f"{self.cross} **I don't have permission to add roles!**")
        except discord.HTTPException:
            return await ctx.send(f"{self.cross} **Something went wrong!**")
        em = discord.Embed(
            title = f"{self.tick} Role added!",
            description = f"{member.mention} has been given {role.mention} role.",
            color = discord.Color.yellow()
        )
        await ctx.send(embed=em)

    @commands.command(aliases=['remover'])
    @commands.has_permissions(manage_roles = True)
    async def removerole(self, ctx, role, member : discord.Member):
        """Removes role from a member"""
        role = discord.utils.get(ctx.guild.roles, name=role)
        if role not in member.roles:
            return await ctx.send(f"**{self.cross} {member} doesn't have have {role} role**")
        try:
            await member.remove_roles(role)
        except discord.Forbidden:
            return await ctx.send(f"{self.cross} **I don't have permission to remove roles!**")
        except discord.HTTPException:
            return await ctx.send(f"{self.cross} **Something went wrong!**")
        await ctx.send(f"Removed role: `{role}`\nFrom: `{member}`\nSir!")

    @commands.command(aliases=['allr'])
    @commands.has_permissions(manage_roles = True)
    async def allroles(self, ctx):
        """List all roles in the guild"""
        em = discord.Embed(
            title = f"Here are all the roles:",
            description = "\n".join([str(role.name) for role in ctx.guild.roles]).replace("@everyone", ""),
            color = discord.Color.blue()
        )
        await ctx.send(embed=em)

    @commands.command(aliases=['memr'])
    @commands.has_permissions(manage_roles = True)
    async def memroles(self, ctx, member : discord.Member):
        """List all roles a user has"""
        try:
            em = discord.Embed(
                title = f"Here are all the roles:",
                description = "\n".join([str(role.name) for role in member.roles]).replace("@everyone", ""),
                color = discord.Color.blue()
            )
            await ctx.send(embed=em)
        except MissingRequiredArgument:
            em = discord.Embed(
                title = f"Here are all the roles:",
                description = "\n".join([str(role.name) for role in ctx.author.roles]).replace("@everyone", ""),
                color = discord.Color.blue()
            )
            await ctx.send(embed=em)
        except MissingPermissions:
            await ctx.send(f"{self.cross} You dont have the permission to do that!")

def setup(bot):
    bot.add_cog(Roles(bot))
