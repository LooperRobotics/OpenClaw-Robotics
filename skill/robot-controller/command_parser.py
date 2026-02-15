"""
Brand-agnostic command parser for robot control.
Converts natural language to unified action commands.
"""

import re
from dataclasses import dataclass
from typing import Optional, List
from enum import Enum


class RobotCategory(Enum):
    QUADRUPED = "quadruped"
    HUMANOID = "humanoid"
    MANIPULATOR = "manipulator"


@dataclass
class ParsedCommand:
    """Parsed command result"""
    raw_command: str
    action: str
    params: dict
    robot_category: RobotCategory
    confidence: float


class CommandParser:
    """Brand-agnostic command parser"""
    
    ACTION_PATTERNS = {
        # Movement
        "forward": [
            r"(向前|前进|往前走|朝前走)(\d+(?:\.\d+)?)米?",
            r"前进(\d+(?:\.\d+)?)米?"
        ],
        "backward": [
            r"(向后|后退|往后走)(\d+(?:\.\d+)?)米?"
        ],
        "turn_left": [
            r"左转(\d+(?:\.\d+)?)度?",
            r"逆时针转(\d+(?:\.\d+)?)度?"
        ],
        "turn_right": [
            r"右转(\d+(?:\.\d+)?)度?",
            r"顺时针转(\d+(?:\.\d+)?)度?"
        ],
        # Posture
        "stand": [
            r"(站起?|起来|站立|站起来)",
            r"起立"
        ],
        "sit": [
            r"坐下",
            r"蹲下"
        ],
        "lie_down": [
            r"躺下",
            r"卧倒"
        ],
        # Arm (humanoid/manipulator)
        "wave": [
            r"挥手",
            r"招手"
        ],
        "handshake": [
            r"握手"
        ],
        "grasp": [
            r"(抓|握|拿起)"
        ],
        "release": [
            r"(放下|松开|释放)"
        ],
        # Navigation
        "go_to": [
            r"去(\d+)[,，](\d+).*位置",
            r"导航到(\d+)[,，](\d+)"
        ],
        # Sensors
        "get_battery": [
            r"(查看|获取)电量"
        ],
        "get_pose": [
            r"(获取|查看)位置"
        ],
        # Stop
        "stop": [
            r"(停止|停下|暂停)"
        ],
    }
    
    def __init__(self):
        self.compiled_patterns = {}
        self._compile_patterns()
    
    def _compile_patterns(self):
        for action, patterns in self.ACTION_PATTERNS.items():
            self.compiled_patterns[action] = [
                re.compile(p) for p in patterns if re.compile(p)
            ]
    
    def parse(self, command: str, robot_type: str = "quadruped") -> ParsedCommand:
        """Parse natural language command"""
        command = command.strip()
        
        # Handle sequence commands
        if "然后" in command or "再" in command or "接着" in command:
            return self._parse_sequence(command, robot_type)
        
        # Single command
        for action, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                match = pattern.search(command)
                if match:
                    params = self._extract_params(action, match, command)
                    return ParsedCommand(
                        raw_command=command,
                        action=action,
                        params=params,
                        robot_category=RobotCategory(robot_type),
                        confidence=0.9
                    )
        
        return ParsedCommand(
            raw_command=command,
            action="unknown",
            params={},
            robot_category=RobotCategory(robot_type),
            confidence=0.0
        )
    
    def _parse_sequence(self, command: str, robot_type: str) -> ParsedCommand:
        """Parse combined commands"""
        parts = re.split(r"(然后|再|接着)+", command)
        tasks = []
        
        for part in parts:
            if part.strip():
                parsed = self.parse(part.strip(), robot_type)
                if parsed.action != "unknown":
                    tasks.append({
                        "action": parsed.action,
                        "params": parsed.params
                    })
        
        return ParsedCommand(
            raw_command=command,
            action="sequence",
            params={"tasks": tasks},
            robot_category=RobotCategory(robot_type),
            confidence=0.85
        )
    
    def _extract_params(self, action: str, match, original: str = "") -> dict:
        """Extract parameters from regex match"""
        params = {}
        
        if action in ["forward", "backward"]:
            try:
                params["distance"] = float(match.group(1)) if match.group(1) else 1.0
            except:
                params["distance"] = 1.0
            params["speed"] = 0.5
                
        elif action == "turn_left":
            try:
                params["angle"] = int(match.group(1)) if match.group(1) else 45
            except:
                params["angle"] = 45
                
        elif action == "turn_right":
            try:
                params["angle"] = -int(match.group(1)) if match.group(1) else -45
            except:
                params["angle"] = -45
                
        elif action == "go_to":
            try:
                if len(match.groups()) >= 2:
                    params["position"] = [float(match.group(1)), float(match.group(2)), 0.0]
            except:
                pass
        
        elif action in ["grasp", "release"]:
            if "左手" in original:
                params["arm"] = "left"
            elif "右手" in original:
                params["arm"] = "right"
            else:
                params["arm"] = "right"
        
        return params
